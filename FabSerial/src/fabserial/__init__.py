#!/usr/bin/env python
# coding=utf-8

__author__ = "Kenichi Ohwada"

import sys
import argparse
from fabserial import Server

def main():
    parser = argparse.ArgumentParser(prog="run")
    parser.add_argument("-b", "--basedir", action="store", dest="basedir",
        help="Specify the basedir to use for uploads, timelapses etc. ")
    parser.add_argument("--port", action="store", type=int, dest="port",
        help="Specify the port on which to bind the server")
    args = parser.parse_args()
    server = Server(args.basedir, args.port)
    server.run()

if __name__ == "__main__":
    main()
