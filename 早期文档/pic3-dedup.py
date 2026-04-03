import os
import shutil
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from tqdm import tqdm

# ================= 配置区域 (请确保都在同一个盘符下!) =================
# 1. 你的源文件夹 (里面包含 Landscape, Portrait 等子文件夹)
SOURCE_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\Final_Album_Organized"

# 2. 最终保留的“精品”文件夹
KEEP_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\Final_Gallery_Clean"

# 3. 淘汰的“重复/低画质”文件夹 (检查后可删除)
TRASH_DIR = r"G:\QQ files\394833062\Image\Sorted_By_BPP\Duplicate_Trash"

# 支持的格式
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.heic'}
MAX_WORKERS = 16
# ===================================================================

def calculate_dhash(image_path, hash_size=8):
    """
    计算 dHash (差值哈希)，只需要读图，不写入
    """
    try:
        with Image.open(image_path) as img:
            # 转换为灰度并缩放，这是计算哈希的标准步骤
            img = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
            pixels = np.array(img)
            diff = pixels[:, 1:] > pixels[:, :-1]
            return hex(int("".join(diff.flatten().astype(int).astype(str)), 2))
    except Exception:
        return None

def get_image_quality_score(file_path):
    """
    计算质量分: 像素越多越好，文件越大越好
    返回: (score, file_path)
    """
    try:
        size = os.path.getsize(file_path)
        with Image.open(file_path) as img:
            width, height = img.size
            # 评分算法：像素数 * 10000 + 文件大小
            # 这样保证分辨率是第一要素，分辨率一样时看文件大小
            score = (width * height) * 10000 + size
            return (score, file_path)
    except:
        return (0, file_path)

def process_file_info(file_path):
    """线程任务：提取哈希和质量"""
    dhash = calculate_dhash(file_path)
    if dhash:
        score, _ = get_image_quality_score(file_path)
        return (dhash, score, file_path)
    return None

def safe_move(src_path, target_root_dir, keep_structure=True):
    """
    执行移动操作 (Move)。
    如果 keep_structure=True，会保持原有的目录层级 (如 /Portrait/Size_L/)
    """
    try:
        if keep_structure:
            # 计算相对路径，例如: 02_Portrait_竖屏\Size_M\img.jpg
            rel_path = os.path.relpath(src_path, SOURCE_DIR)
            dest_path = os.path.join(target_root_dir, rel_path)
        else:
            # 如果不保持结构（用于垃圾桶），直接扔进去
            filename = os.path.basename(src_path)
            dest_path = os.path.join(target_root_dir, filename)

        dest_folder = os.path.dirname(dest_path)
        os.makedirs(dest_folder, exist_ok=True)

        # 处理重名冲突 (移动而非覆盖)
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(os.path.basename(src_path))
            counter = 1
            while os.path.exists(dest_path):
                new_name = f"{base}_dup_{counter}{ext}"
                dest_path = os.path.join(dest_folder, new_name)
                counter += 1
        
        shutil.move(src_path, dest_path)
        return True
    except Exception as e:
        print(f"移动失败 {src_path}: {e}")
        return False

def main():
    # 安全检查
    if os.path.splitdrive(SOURCE_DIR)[0] != os.path.splitdrive(KEEP_DIR)[0]:
        print("⚠️ 警告：源文件夹和目标文件夹不在同一个盘符！")
        print("这会导致文件‘复制并删除’，从而产生磁盘写入。")
        print("建议修改路径，确保它们在同一个分区 (例如都在 D: 盘)。")
        input("按 Enter 继续 (如果不在乎写入)，或 Ctrl+C 退出...")

    print(f"正在扫描: {SOURCE_DIR}")
    
    # 1. 收集文件
    all_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if os.path.splitext(file)[1].lower() in VALID_EXTENSIONS:
                all_files.append(os.path.join(root, file))
    
    total_files = len(all_files)
    if total_files == 0: return

    print(f"找到 {total_files} 个文件，开始计算指纹...")

    # 2. 并发计算哈希
    # 结构: { hash_str: [ (score, path), (score, path) ... ] }
    hash_groups = defaultdict(list)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_file_info, f) for f in all_files]
        
        for future in tqdm(as_completed(futures), total=total_files, unit="img"):
            res = future.result()
            if res:
                dhash, score, path = res
                hash_groups[dhash].append((score, path))

    print(f"\n指纹计算完成。开始执行 0 损耗移动...")

    # 3. 分类与移动
    moved_keep = 0
    moved_trash = 0
    
    # 将字典转换为列表处理，方便显示进度
    groups = list(hash_groups.values())
    
    for group in tqdm(groups, unit="grp"):
        # 按分数降序排列：分数最高的排第一个
        group.sort(key=lambda x: x[0], reverse=True)
        
        # 冠军 (Winner) -> 移动到保留区
        winner_score, winner_path = group[0]
        safe_move(winner_path, KEEP_DIR, keep_structure=True)
        moved_keep += 1
        
        # 输家 (Losers) -> 移动到垃圾桶
        # 如果 group 长度 > 1，说明有重复
        for i in range(1, len(group)):
            loser_score, loser_path = group[i]
            # 垃圾桶里不需要保持目录结构，直接平铺扔进去即可，或者保持也可以
            # 这里选择 keep_structure=True 方便你万一想找回，知道它是哪类的
            safe_move(loser_path, TRASH_DIR, keep_structure=True)
            moved_trash += 1

    print("-" * 30)
    print(f"✅ 处理完成！硬盘寿命已保护。")
    print(f"保留并归档 (Winner): {moved_keep} 张 -> {KEEP_DIR}")
    print(f"移入垃圾桶 (Losers): {moved_trash} 张 -> {TRASH_DIR}")
    print("-" * 30)
    print("提示：请检查 'Duplicate_Trash' 文件夹，确认无误后可直接删除以释放空间。")
    print("原文件夹现在应该是空的（除了空文件夹本身）。")

if __name__ == "__main__":
    main()