#!/bin/bash

function Exit {
    exit
}

function Usage {
    echo "Usage: $(basename $0) <option>"
    echo 
    echo "至少需要指定以下一个选项："
    echo "  -a,--all                : 处理所有表情包目录。"
    echo "  -d,--dir <directory>    : 处理单个表情包目录。"
    echo "  -h,--help               : 显示帮助信息。"
    Exit
}


function Branch {
    git branch "$_name_"
    git checkout --orphan "$_name_"
    git rm --cached -r .
    git clean -f -d
    git checkout master "$_dir_"
    git commit -m "$(date)"
    git checkout master
}


if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
    echo "Usage Error!"
    Usage
else
    for (( i=1; i<=$#; ++i )) do
		case "${!i}" in
			"-a" | "--all")
				for i in image/* ; do
                    _dir_="${!i}"
                    _name_="$(basename ${!i})"
                    Branch
                done
                Exit
				;;
			"-d" | "--dir")
				((++i))
				_dir_="${!i}"
                _name_="$(basename ${!i})"
                Branch
                Exit
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
