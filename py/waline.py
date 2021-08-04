import os
import json
import argparse

IMAGE_SUFFIX = ['.png', '.jpg', '.jpeg', '.gif', '.webp']

# 扫描单层目录下所有表情包
def scanDir(repo, dir, cdn):
    info = {}
    info['name'] = os.path.basename(dir)
    info['folder'] = os.path.join(cdn, f"{repo}@{info['name']}", dir.split(f'/{repo}/')[1].strip("/"))
    info['items'] = []
    for file in sorted(os.listdir(dir)):
        if os.path.splitext(file)[-1].lower() in IMAGE_SUFFIX:
            info['items'].append(file)
    
    info['icon'] = info['items'][0]
    return info


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
    emojiCDN = 'https://cdn.jsdelivr.net/gh/hotarugali/'

    if args.all:
        for file in os.listdir(image):
            dir = os.path.join(image, file)
            if os.path.isdir(dir):
                info = scanDir(repo, dir, emojiCDN)
                infoDir = os.path.join(waline, file)
                os.makedirs(infoDir, exist_ok=True)
                with open(os.path.join(infoDir, "info.json"), "w") as f:
                    json.dump(info, f, indent=4)
    
    if args.dir is not None:
        assert os.path.exists(args.dir), "错误：路径不存在！"
        assert os.path.isdir(args.dir), "错误：不是目录！"
        args.dir = os.path.join(image, os.path.basename(args.dir))
        assert os.path.exists(args.dir), "错误：表情包目录不在 '{}' 目录下！".format(image)

        info = scanDir(repo, args.dir, emojiCDN)
        infoDir = os.path.join(waline, os.path.basename(args.dir))
        os.makedirs(infoDir, exist_ok=True)
        with open(os.path.join(infoDir, "info.json"), "w") as f:
            json.dump(info, f, indent=4)
