#!/usr/bin/env python
# coding=utf-8

__author__ = "Kenichi Ohwada"

import os
import sys

basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(basedir, "src"))

import fabprinter
fabprinter.main()
