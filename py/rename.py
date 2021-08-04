## 该脚本主要用于对表情包文件重命名
## 防止评论加载不同类别表情包文件时产生命名冲突

import os
import shutil
import argparse

IMAGE_SUFFIX = ['.png', '.jpg', 'jpeg', '.gif', '.webp']

# 对表情包文件重命名
def rename(dir, args):
    count = 0
    name = os.path.basename(dir)
    for file in os.listdir(dir):
        suffix = os.path.splitext(file)[-1]
        if suffix.lower() in IMAGE_SUFFIX:
            src_path = os.path.join(dir, file)
            dst_path = os.path.join(dir, f'{name}_{file}')
            if args.serial:
                count += 1
                dst_path = os.path.join(dir, f'{name}_{count}{suffix}')

            os.rename(src_path, dst_path)


if __name__=='__main__':
    # 读取命令行参数
    parse = argparse.ArgumentParser()
    parse = parse.add_argument('--serial', '-s', action='store_true', default=False, help='是否对表情包文件进行数字化序列命名。')
    group = parse.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', '-a', action='store_true', default=False, help='是否同时处理所有表情包目录。')
    group.add_argument('--dir', '-d', type=str, default=None, help='指定单个表情包目录进行处理。')
    args = parse.parse_args()

    # 处理表情包
    repo = 'Emoji'
    path = os.path.dirname(os.path.abspath(__file__))
    image = os.path.normpath(os.path.join(path, "../image"))

    if args.all:
        for file in os.listdir(image):
            dir = os.path.join(image, file)
            if os.path.isdir(dir):
                rename(dir, args)
    
    if args.dir is not None:
        assert os.path.exists(args.dir), "错误：路径不存在！"
        assert os.path.isdir(args.dir), "错误：不是目录！"
        args.dir = os.path.join(image, os.path.basename(args.dir))
        assert os.path.exists(args.dir), "错误：表情包目录不在 '{}' 目录下！".format(image)

        rename(args.dir, args)