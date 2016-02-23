#!/bin/sh
# Author: Kenichi Ohwada

cp scripts/fabserial.init /etc/init.d/fabserial
chmod 755 /etc/init.d/fabserial
cp scripts/fabserial.default /etc/default/fabserial
chmod 644 /etc/default/fabserial
insserv fabserial
