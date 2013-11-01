#!/bin/sh

mkdir -p /usr/share/nginx/html/test
cd /usr/share/nginx/html/test

dd if=/dev/urandom of=file-10K.dat bs=10K count=1
dd if=/dev/urandom of=file-100K.dat bs=100K count=1
dd if=/dev/urandom of=file-1M.dat bs=1M count=1
dd if=/dev/urandom of=file-10M.dat bs=10M count=1

wget -N http://dev1.mdw.la/test/warmup.html
wget -N http://dev1.mdw.la/test/test_1KB.jpg
wget -N http://dev1.mdw.la/test/test_10KB.jpg
wget -N http://dev1.mdw.la/test/test_100KB.jpg
wget -N http://dev1.mdw.la/test/test_1MB.jpg
wget -N http://dev1.mdw.la/test/ten_img.html

mkdir imgs
cd imgs

wget -N http://dev1.mdw.la/test/imgs/test_100KB_0.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_1.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_2.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_3.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_4.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_5.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_6.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_7.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_8.jpg
wget -N http://dev1.mdw.la/test/imgs/test_100KB_9.jpg

rm -rf /tmp/quic-data
mkdir -p /tmp/quic-data
cd /tmp/quic-data

wget -p --save-headers http://quic-server/test/file-10K.dat
wget -p --save-headers http://quic-server/test/file-100K.dat
wget -p --save-headers http://quic-server/test/file-1M.dat
wget -p --save-headers http://quic-server/test/file-10M.dat
wget -p --save-headers http://quic-server/test/warmup.html
wget -p --save-headers http://quic-server/test/test_1KB.jpg
wget -p --save-headers http://quic-server/test/test_10KB.jpg
wget -p --save-headers http://quic-server/test/test_100KB.jpg
wget -p --save-headers http://quic-server/test/test_1MB.jpg
wget -p --save-headers http://quic-server/test/ten_img.html
wget -p --save-headers http://quic-server/test/imgs/test_100KB_0.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_1.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_2.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_3.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_4.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_5.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_6.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_7.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_8.jpg
wget -p --save-headers http://quic-server/test/imgs/test_100KB_9.jpg
