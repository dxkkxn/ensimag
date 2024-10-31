#!/usr/bin/env sh

# while true
# do
    nc -lp 5000 > /tmp/file_in.txt; # listen in port 5000
    echo "im the snitcher" > /tmp/file_out.txt
    cat /tmp/file_in.txt >> /tmp/file_out.txt
    nc -lp 6000 < /tmp/file_out.txt # send file to port 6000
# done
