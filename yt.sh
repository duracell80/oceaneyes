yt-dlp -f $2 https://www.youtube.com/watch?v=$1 -o - | ffmpeg -v quiet -hide_banner -loglevel quiet -nostats -re -i pipe:0 -vn -codec:a libmp3lame -b:a 192k -f mp3 -content_type audio/mpeg icecast://source:$5@$3:$4/ytradio-$1 &

# wget https://radios.yt/genre/classical/?X-Requested-With=rytXMLHttpRequest
# cat index.html\?X-Requested-With\=rytXMLHttpRequest | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" | sort -u | grep -i "ytimg" | sed 's|i.ytimg.com/vi/|youtube.com/watch?v=|g' | sed 's|/hqdefault_live.jpg||g'

