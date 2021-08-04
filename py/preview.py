import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from airium import Airium

# 扫描单层目录下所有表情包
def scanDir(repo, dir):
    files = sorted(os.listdir(dir))
    folder = dir.split(repo)[1].strip("/")
    cols = 6
    rows = (len(files)-1) // cols + 1
    height = 120
    width = 120
    readme = Airium()
    with readme.table(border='0'):
        for row in range(rows):
            with readme.tr().td(align='center'):
                for col in range(cols):
                    index = row*cols + col
                    if index < len(files):
                        readme.img(src=os.path.join("../..", folder), height=f"{height}", width=f"{width}")
    return str(readme)

if __name__=='__main__':
    repo = 'Emoji'
    path = os.getcwd()
    image = os.path.normpath(os.path.join(path, "../image"))
    preview = os.path.normpath(os.path.join(path, "../preview"))
    for file in os.listdir(image):
        dir = os.path.join(image, file)
        if os.path.isdir(dir):
            readme = scanDir(repo, dir)
            readmeDir = os.path.join(preview, file)
            os.makedirs(readmeDir, exist_ok=True)
            with open(os.path.join(readmeDir, "README.md"), "w") as f:
                f.write(readme)
