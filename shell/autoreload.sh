#!/bin/sh

objectdir="/data/www/xtyw"
# 启动inotify监视项目目录， 参数"--exclude" 为忽略的文件或目录正则
/usr/bin/inotifywait -mrq --exclude "(static|logs|shell|\.swap|\.pyc|\.swx|\.py\~)" --timefmt '%d/%m/%y %H:%M' --format '%T %w%f' --event modify,delete,move,create,attrib ${objectdir} | while read files
do
/bin/touch /data/www/xtyw/shell/reload.set
    continue
done &
