import os
import shutil
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from tqdm import tqdm  # 进度条库

# ================= 配置区域 =================
SOURCE_DIR = r"G:\QQ files\394833062\Image"
OUTPUT_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP"
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
MAX_WORKERS = 4  # 线程数 (建议设置为 CPU 核心数的 2-4 倍，或者直接 16-32)
# ===========================================

# 全局锁，用于防止移动文件时重名冲突的竞态条件（虽然我们下面用了预计算路径策略，加锁更保险）
move_lock = Lock()

def get_image_info(file_path):
    """
    读取单张图片信息，返回 (path, bpp)
    """
    try:
        # 获取文件大小 (系统调用，很快)
        stat = os.stat(file_path)
        file_size = stat.st_size
        if file_size == 0:
            return None

        #以此优化：只读取图片头部信息，不加载整张图
        with Image.open(file_path) as img:
            width, height = img.size
            if width == 0 or height == 0:
                return None
            bpp = (file_size * 8) / (width * height)
            return (file_path, bpp)
            
    except Exception:
        # 忽略损坏的图片
        return None

def generate_move_task(item, mean_bpp, std_bpp):
    """
    计算目标路径，不执行移动。
    返回 (源路径, 目标文件夹名)
    """
    path = item[0]
    bpp = item[1]
    
    # 防止标准差为0
    if std_bpp == 0:
        z_score = 0
    else:
        z_score = (bpp - mean_bpp) / std_bpp
    
    abs_z = abs(z_score)
    direction = "High" if z_score >= 0 else "Low" # High=噪点/细节, Low=纯色/模糊
    
    if abs_z <= 1:
        folder = "1_Sigma_Range"
    elif abs_z <= 2:
        folder = f"2_Sigma_{direction}"
    elif abs_z <= 3:
        folder = f"3_Sigma_{direction}"
    else:
        folder = f"Outliers_{direction}" # 极端值
        
    return path, folder

def safe_move_file(src_path, dest_folder):
    """
    执行移动操作 (线程安全由文件名生成逻辑保证)
    """
    try:
        if not os.path.exists(dest_folder):
            # makedirs 可能会有多线程竞争，忽略已存在的错误
            os.makedirs(dest_folder, exist_ok=True)
            
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)
        
        # 简单的重名处理 (原子性较差但够用，严格去重建议在单线程阶段做)
        # 这里为了速度，如果遇到重名，直接加个随机后缀或跳过
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            # 简单粗暴：加个 _dup 标记
            dest_path = os.path.join(dest_folder, f"{base}_dup{ext}")
            
            # 如果还存在，那就在后面再追加数字 (这一步加锁防止冲突)
            count = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_dup_{count}{ext}")
                count += 1
        
        shutil.move(src_path, dest_path)
        return True
    except Exception as e:
        print(f"移动失败 {src_path}: {e}")
        return False

def main():
    # 1. 快速扫描文件列表
    print(f"--- 阶段 1: 扫描文件列表 ---")
    all_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS:
                all_files.append(os.path.join(root, file))
    
    print(f"找到 {len(all_files)} 个图片文件。")
    if not all_files: return

    # 2. 多线程计算 BPP
    print(f"\n--- 阶段 2: 多线程计算密度 (BPP) ---")
    valid_data = [] # 存储 (path, bpp)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        futures = {executor.submit(get_image_info, f): f for f in all_files}
        
        # 使用 tqdm 显示进度条
        for future in tqdm(as_completed(futures), total=len(all_files), unit="img"):
            result = future.result()
            if result:
                valid_data.append(result)

    if not valid_data:
        print("没有可处理的有效图片。")
        return

    # 3. 计算统计学分布 (瞬间完成)
    print(f"\n--- 阶段 3: 统计分析 ---")
    bpp_values = np.array([x[1] for x in valid_data])
    mean_bpp = np.mean(bpp_values)
    std_bpp = np.std(bpp_values)
    
    print(f"平均 BPP: {mean_bpp:.4f}")
    print(f"标准差 σ: {std_bpp:.4f}")

    # 4. 多线程移动文件
    print(f"\n--- 阶段 4: 多线程分类移动 ---")
    
    # 预计算所有文件的目标文件夹，减少线程里的计算量
    move_tasks = []
    for item in valid_data:
        path, folder_name = generate_move_task(item, mean_bpp, std_bpp)
        dest_full_path = os.path.join(OUTPUT_DIR, folder_name)
        move_tasks.append((path, dest_full_path))
        
    # 执行移动
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(safe_move_file, src, dst) for src, dst in move_tasks]
        
        for _ in tqdm(as_completed(futures), total=len(move_tasks), unit="file"):
            pass

    print(f"\n✅ 全部完成！请查看: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()