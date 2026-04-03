import os
import shutil
from PIL import Image, ExifTags
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ================= 配置区域 (确保在同一盘符!) =================
# 1. 输入: 上一步整理好的干净相册
SOURCE_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\Final_Gallery_Clean"

# 2. 输出: 存放识别出来的截图 (保持原有目录结构)
SCREENSHOT_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\Separated_Screenshots"

# 3. 判定阈值 (0.0 ~ 1.0)
# 如果图片中"独特颜色数量 / 总像素数"低于此值，被判定为截图
# 0.15 是一个经验值：照片通常在 0.3 以上，UI截图通常在 0.05 以下
COLOR_COMPLEXITY_THRESHOLD = 0.15 

# 支持的格式
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.heic'}
MAX_WORKERS = 16
# =============================================================

def has_camera_exif(img):
    """
    检查是否有物理摄像头的 EXIF 信息 (光圈、ISO、快门)
    这是判断"真实照片"的最强证据。
    """
    try:
        exif = img._getexif()
        if not exif:
            return False
        
        # 建立 Tag ID 到名称的映射
        exif_data = {ExifTags.TAGS.get(k, k): v for k, v in exif.items()}
        
        # 检查关键物理参数。如果存在这些，几乎肯定是相机拍的
        # ISOSpeedRatings (34855), FNumber (33437), ExposureTime (33434)
        physical_tags = ['ISOSpeedRatings', 'FNumber', 'ExposureTime', 'FocalLength']
        
        for tag in physical_tags:
            if tag in exif_data:
                return True
                
        # 检查相机制造商 (Make/Model)
        # 截图通常没有 Make，或者 Make 是软件名
        if 'Make' in exif_data:
            make = str(exif_data['Make']).lower()
            # 排除一些软件生成的标记
            if 'android' not in make and 'gimp' not in make and 'photoshop' not in make:
                return True
                
        return False
    except Exception:
        return False

def analyze_image_content(file_path):
    """
    核心算法：分析图片是"渲染生成的(截图)"还是"由于光线拍摄的(照片)"
    返回: True (是截图), False (是照片)
    """
    try:
        with Image.open(file_path) as img:
            # 1. 优先检查 EXIF (一票否决权)
            # 如果有确凿的相机参数，直接认定为照片，不当截图处理
            if has_camera_exif(img):
                return False 

            # 2. 颜色复杂度分析 (Color Complexity)
            # 为了速度，也为了忽略噪点，我们先缩小图片
            # 缩放到 256px 宽，既能保留 UI 结构，又能统计颜色分布
            img_small = img.resize((256, 256), resample=Image.Resampling.BOX)
            
            # 强制转为 RGB (去除 Alpha 通道干扰)
            img_rgb = img_small.convert("RGB")
            
            # 获取所有独特的颜色数量
            # maxcolors 设为像素总数，保证能数全
            colors = img_rgb.getcolors(maxcolors=256*256)
            
            if not colors:
                return True # 获取失败通常是因为格式奇怪，归为非照片

            unique_color_count = len(colors)
            total_pixels = 256 * 256
            
            # 计算"颜色杂乱度"比率
            complexity_ratio = unique_color_count / total_pixels
            
            # 判定逻辑：
            # 截图 (UI/文字/矢量图): 颜色非常纯，独特颜色很少 (Ratio < 0.1)
            # 照片 (自然光/纹理): 哪怕是纯黑图片，由于传感器噪声，独特颜色也很多 (Ratio > 0.2)
            if complexity_ratio < COLOR_COMPLEXITY_THRESHOLD:
                return True # 是截图
            else:
                return False # 是照片
                
    except Exception as e:
        print(f"无法读取 {file_path}: {e}")
        return False # 读不出来的保守起见不动它

def safe_move(src_path, target_root_dir):
    """
    移动文件并保持目录结构
    """
    try:
        # 计算相对路径，例如: Landscape\Size_L\img.png
        rel_path = os.path.relpath(src_path, SOURCE_DIR)
        dest_path = os.path.join(target_root_dir, rel_path)
        
        dest_folder = os.path.dirname(dest_path)
        os.makedirs(dest_folder, exist_ok=True)

        if os.path.exists(dest_path):
            base, ext = os.path.splitext(os.path.basename(src_path))
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_scr_{counter}{ext}")
                counter += 1
        
        shutil.move(src_path, dest_path)
        return True
    except Exception as e:
        print(f"移动失败 {src_path}: {e}")
        return False

def process_task(file_path):
    """线程任务"""
    is_screenshot = analyze_image_content(file_path)
    return (file_path, is_screenshot)

def main():
    # 再次检查盘符，确保 0 损耗
    if os.path.splitdrive(SOURCE_DIR)[0] != os.path.splitdrive(SCREENSHOT_DIR)[0]:
        print("⚠️ 警告：源目录和目标目录不在同一个盘符！移动操作将涉及大量写入。")
        input("按 Enter 继续，或 Ctrl+C 退出...")

    print(f"正在分析图库: {SOURCE_DIR}")
    print(f"判定阈值 (颜色复杂度): < {COLOR_COMPLEXITY_THRESHOLD}")
    
    all_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if os.path.splitext(file)[1].lower() in VALID_EXTENSIONS:
                all_files.append(os.path.join(root, file))
    
    total = len(all_files)
    if total == 0: return

    print(f"开始智能分析 {total} 张图片...")
    
    screenshot_count = 0
    photo_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_task, f) for f in all_files]
        
        for future in tqdm(as_completed(futures), total=total, unit="img"):
            file_path, is_screenshot = future.result()
            
            if is_screenshot:
                # 移动到截图文件夹
                if safe_move(file_path, SCREENSHOT_DIR):
                    screenshot_count += 1
            else:
                # 照片留在原地 (Do nothing)
                photo_count += 1

    print("-" * 30)
    print(f"✅ 分类完成！")
    print(f"📸 保留照片 (原地不动): {photo_count} 张")
    print(f"📱 移走截图 (Separated): {screenshot_count} 张")
    print(f"截图存放位置: {SCREENSHOT_DIR}")
    print("-" * 30)
    print("原理说明：")
    print("1. 如果有光圈/快门/ISO信息，判定为照片。")
    print("2. 如果颜色分布过于纯净（无传感器噪点），判定为截图。")

if __name__ == "__main__":
    main()