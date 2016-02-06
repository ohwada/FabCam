#!/bin/sh
# Author: Kenichi Ohwada

cp scripts/fabcam.init /etc/init.d/fabcam
chmod 755 /etc/init.d/fabcam
cp scripts/fabcam.default /etc/default/fabcam
chmod 644 /etc/default/fabcam
insserv fabcam
