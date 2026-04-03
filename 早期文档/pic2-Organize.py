import os
import shutil
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ================= 配置区域 =================
# 输入文件夹 (指向上一步生成的 1_Sigma_Range 文件夹)
SOURCE_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\1_Sigma_Range"

# 输出文件夹 (最终整理好的相册根目录)
OUTPUT_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\Final_Album_Organized"

# 支持的格式
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.heic'}
MAX_WORKERS = 16
# ===========================================

def get_image_dims(file_path):
    """
    只读取图片头部，获取 (宽, 高)
    """
    try:
        with Image.open(file_path) as img:
            return img.size
    except Exception:
        return None

def classify_image(width, height):
    """
    核心分类逻辑
    返回: (第一层文件夹名, 第二层文件夹名)
    """
    # 1. 第一层：画幅比例 (Aspect Ratio)
    ratio = width / height
    
    if 0.95 <= ratio <= 1.05:
        aspect_folder = "03_Square_方形"
    elif ratio > 1.05:
        aspect_folder = "01_Landscape_横屏"
    else:
        aspect_folder = "02_Portrait_竖屏"

    # 2. 第二层：分辨率大小 (Resolution)
    # 使用长边作为判断标准，比较符合直觉
    long_side = max(width, height)
    
    if long_side < 1000:
        res_folder = "Size_S_Small"    # < 1000px
    elif long_side < 2000:
        res_folder = "Size_M_Medium"   # 1000-2000px
    elif long_side < 4000:
        res_folder = "Size_L_Large"    # 2000-4000px
    else:
        res_folder = "Size_XL_Ultra"   # > 4000px

    return aspect_folder, res_folder

def process_and_move(file_path):
    """
    处理单个文件的任务函数
    """
    dims = get_image_dims(file_path)
    if not dims:
        return False # 无法读取

    width, height = dims
    aspect_folder, res_folder = classify_image(width, height)
    
    # 构建目标路径: OUTPUT / 画幅 / 分辨率 / 文件名
    target_dir = os.path.join(OUTPUT_DIR, aspect_folder, res_folder)
    
    try:
        os.makedirs(target_dir, exist_ok=True)
        
        filename = os.path.basename(file_path)
        dest_path = os.path.join(target_dir, filename)
        
        # 简单的重名处理
        if os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                counter += 1
        
        shutil.move(file_path, dest_path)
        return True
    except Exception as e:
        print(f"移动出错 {file_path}: {e}")
        return False

def main():
    print(f"正在扫描文件夹: {SOURCE_DIR}")
    
    # 1. 收集所有文件路径
    all_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS:
                all_files.append(os.path.join(root, file))
    
    total_files = len(all_files)
    print(f"找到 {total_files} 张图片，准备分类...")
    
    if total_files == 0:
        print("文件夹为空，无需处理。")
        return

    # 2. 多线程处理
    # 这里的任务是 IO 密集型 (读头 -> 移动)，适合多线程
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交任务
        futures = [executor.submit(process_and_move, f) for f in all_files]
        
        # 进度条
        for future in tqdm(as_completed(futures), total=total_files, unit="img"):
            if future.result():
                success_count += 1
                
    print(f"\n✅ 整理完成！")
    print(f"成功移动: {success_count}/{total_files}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("文件夹结构预览:")
    print("  └─ 01_Landscape_横屏")
    print("      └─ Size_M_Medium (例如)")
    print("  └─ 02_Portrait_竖屏")
    print("  └─ 03_Square_方形")

if __name__ == "__main__":
    main()