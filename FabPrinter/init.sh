#!/bin/sh
# Author: Kenichi Ohwada

cp scripts/fabprinter.init /etc/init.d/fabprinter
chmod 755 /etc/init.d/fabprinter
cp scripts/fabprinter.default /etc/default/fabprinter
chmod 644 /etc/default/fabprinter
insserv fabprinter
