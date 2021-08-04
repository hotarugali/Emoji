#!/bin/bash

function Usage {
    echo "Usage: $(basename $0) <option>"
    echo 
    echo "至少需要指定以下一个选项："
    echo "  -a,--all                : 处理所有表情包目录。"
    echo "  -d,--dir <directory>    : 处理单个表情包目录。"
    echo "  -h,--help               : 显示帮助信息。"
}

function Branch {
    set -x
    if git checkout --orphan "$_name_"; then
        git rm --cached -rf .
        git clean -f -d
        git checkout master "$_dir_"
        git add . && git commit -m "$(date)"
        git checkout master
    fi
}

_path_=$(dirname $0)
pushd "$_path_" > /dev/null
git add . && git commit -m "$(date)"
if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
    echo "Usage Error!"
    Usage
else
    for (( i=1; i<=$#; ++i )) do
		case "${!i}" in
			"-a" | "--all")
				for img in image/* ; do
                    _dir_="$img"
                    _name_="$(basename $img)"
                    echo $_dir_
                    echo $_name_
                    Branch
                done
                break
				;;
			"-d" | "--dir")
				((++i))
				_dir_="${!i}"
                _name_="$(basename ${!i})"
                Branch
                break
				;;
			"-h" | "--help")
				((++i))
				Usage
				;;
			*)
				echo "Usage Error"
				echo "Invalid option: ${!i}"
				Usage
				;;
		esac
	done
fi
git push --all origin
popd > /dev/null