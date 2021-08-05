## 该脚本用于修改表情包库后刷新 jsdelivr 缓存
## 主要是刷新 info.json 文件

import os
import requests
import argparse

# 刷新表情包目录的 jsdelivr 缓存
def refresh(dir, cdn):
    name = os.path.basename(dir)
    url = os.path.join(cdn, f"{repo}@{name}", dir.split(f'/{repo}/')[1].strip("/"))
    print(url)
    requests.get(url)


if __name__=='__main__':
    # 读取命令行参数
    parse = argparse.ArgumentParser()
    group = parse.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', '-a', action='store_true', default=False, help='是否同时处理所有表情包目录。')
    group.add_argument('--dir', '-d', type=str, default=None, help='指定单个表情包目录进行处理。')
    args = parse.parse_args()

    # 处理表情包
    repo = 'Emoji'
    path = os.path.dirname(os.path.abspath(__file__))
    image = os.path.normpath(os.path.join(path, "../image"))
    waline = os.path.normpath(os.path.join(path, "../waline"))
    emojiCDN = 'https://purge.jsdelivr.net/gh/hotarugali/'

    if args.all:
        for file in os.listdir(image):
            dir = os.path.join(image, file)
            if os.path.isdir(dir):
                refresh(dir, emojiCDN)
        for file in os.listdir(waline):
            dir = os.path.join(waline, file)
            if os.path.isdir(dir):
                refresh(dir, emojiCDN)
    
    if args.dir is not None:
        assert os.path.exists(args.dir), "错误：路径不存在！"
        assert os.path.isdir(args.dir), "错误：不是目录！"
        args.dir = os.path.join(waline, os.path.basename(args.dir))
        assert os.path.exists(args.dir), "错误：表情包目录不在 '{}' 目录下！".format(waline)

        image_path = args.dir
        waline_path = os.path.join(waline, os.path.basename(image_path))
        refresh(image_path, emojiCDN)
        refresh(waline_path, emojiCDN)
