import os


def rename_files(directory):
    # 获取文件夹中的所有文件
    files = os.listdir(directory)

    # 排序文件，确保按顺序重命名
    files.sort()

    # 遍历文件并按序号重命名
    for idx, filename in enumerate(files):
        # 生成新的文件名
        new_name = f"{idx}.mp4"  # 假设文件是 .jpg，如果不同可以调整扩展名
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)

        # 重命名文件
        os.rename(src, dst)
        print(f"文件 '{filename}' 已重命名为 '{new_name}'")

        # 停止在 100 个文件后
        if idx >= 100:
            break


# 使用指定的文件夹路径
if __name__ == "__main__":
    directory = r"/Users/a0000/Desktop/myproject/assistant/douyin_upload/video"  # 将此路径替换为你的实际文件夹路径
    rename_files(directory)
