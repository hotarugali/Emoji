import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json

IMAGE_SUFFIX = ['.png', '.jpg', 'jpeg', '.gif', '.webp']

# 扫描单层目录下所有表情包
def scanDir(repo, dir, cdn):
    info = {}
    info['name'] = os.path.basename(dir)
    info['folder'] = os.path.join(cdn, dir.split(f'/{repo}/')[1].strip("/"))
    info['items'] = []
    for file in sorted(os.listdir(dir)):
        if os.path.splitext(file)[-1].lower() in IMAGE_SUFFIX:
            info['items'].append(file)
    
    info['icon'] = info['items'][0]
    return info

if __name__=='__main__':
    repo = 'Emoji'
    path = os.getcwd()
    image = os.path.normpath(os.path.join(path, "../image"))
    waline = os.path.normpath(os.path.join(path, "../waline"))
    emojiCDN = 'https://cdn.jsdelivr.net/gh/hotarugali/Emoji@master/'
    for file in os.listdir(image):
        dir = os.path.join(image, file)
        if os.path.isdir(dir):
            info = scanDir(repo, dir, emojiCDN)
            infoDir = os.path.join(waline, file)
            os.makedirs(infoDir, exist_ok=True)
            with open(os.path.join(infoDir, "info.json"), "w") as f:
                json.dump(info, f, indent=4)
