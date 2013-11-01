#!/bin/sh

cd /tmp/quic-data
quic_server --port=6121 --quic_in_memory_cache_dir=. &> /dev/null
