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
            with readme.tr():
                for col in range(cols):
                    index = row*cols + col
                    if index < len(files):
                        readme.td(align='center').img(src=os.path.join("../..", folder, files[index]), height=f"{height}", width=f"{width}")
    return str(readme)+"\n", files

# 所有目录表情包总览
def summary(repo, emojis):
    cols = 3
    rows = (len(emojis)-1) // cols
    height = 200
    width = 200
    readme = Airium()
    with readme.table(border='1.5'):
        for row in range(rows):
            with readme.tr().td().table(border='1.0'):
                with readme.tr():
                    for col in range(cols):
                        index = row*cols + col
                        if index < len(emojis):
                            readme.td(align='center').img(src=os.path.join("..", emojis[index]['icon'].split(repo)[1].strip("/")), height=f"{height}", width=f"{width}")
                with readme.tr():
                    for col in range(cols):
                        index = row*cols + col
                        if index < len(emojis):
                            readme.td().p(align="center", style=f"width: {width}px;").b(_t=emojis[index]['name'])
    return str(readme)+"\n"


if __name__=='__main__':
    repo = 'Emoji'
    path = os.getcwd()
    image = os.path.normpath(os.path.join(path, "../image"))
    preview = os.path.normpath(os.path.join(path, "../preview"))
    emojis = []
    # 对每类表情包生成对应的预览
    for file in os.listdir(image):
        dir = os.path.join(image, file)
        if os.path.isdir(dir):
            readme, name = scanDir(repo, dir)
            readmeDir = os.path.join(preview, file)
            os.makedirs(readmeDir, exist_ok=True)
            with open(os.path.join(readmeDir, "README.md"), "w") as f:
                f.write(readme)
            
            emojis.append({ 'name': file, 'icon': os.path.join(dir, name[0]) })

    # 对所有表情包生成总览
    readme = summary(repo, emojis)
    with open(os.path.join(preview, "README.md"), "w") as f:
        f.write(readme)