Protocol Benchmarking
============

These scripts provide an easy way to benchmark different protocols, over different network conditions, while reporting the results to a folder in Google Drive.

The current focus in these scripts is to compare Google's QUIC (http://en.wikipedia.org/wiki/QUIC) with regular HTTP and HTTPS.


Getting Started
=============
You'll need two Linux machines for these tests, and the Google QUIC demo client and server binaries (quic_client and quic_server).  One machine will run the tests, and  will act as the client, while the other machine will act as the server.  For testing different network conditions, you will also need a router running OpenWrt and the WAN emulation packages available here: https://github.com/Connectify/openwrt-netem

Compiling the QUIC Demo Client and Server
=============
Excellent instructions are available here: https://code.google.com/p/chromium/wiki/LinuxBuildInstructions

If the client will need to reach the server on IPv4, the quic_server source must be patched to listen for IPv4 requests.  The patch for this is available in the patches directory.  From within the chromium src directory, run this:
```
patch -p1 < path/to/benchmarking/quic-patches/001-quic-server-ipv4.patch
```

Once you have the code, compile the QUIC demo client and server with
```
ninja -C out/Debug quic_client quic_server
```

Setting up the Server
=============
It is assumed that the server will run nginx on port 80 (and 443, if you care to test HTTPS).  Any web server will do, but the file scripts/mk-quic-data.sh will generate some random files, and will download files referenced in the benchmarking in the Chromium source, and currently places them where nginx ought to be looking for them by default.

The domain name _quic-server_ is used by the tests, so you will want to add an entry for quic-server, with the server's address, to /etc/hosts on both the client and server.

Once the files are available on the server, scripts/run-quic-server.sh will run the QUIC server.


Running the tests
==============
A few system environment variables are used by the test.

- GDOCS_USER is a valid Google Docs user
- GDOCS_PW is that user's password
- NETEM_USER is the user for the OpenWrt router (typically root)
- NETEM_PW is the OpenWrt user's password
- NETEM_IP is the IP address of the OpenWrt router
- QUIC_SERVER_IP is the IP address of the QUIC server

Once those environment variables are set, the tests can be run with the following command:
```
python quic_tests.py Test.test_QUIC_vs_HTTP
```
