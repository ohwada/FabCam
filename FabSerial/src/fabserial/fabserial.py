# -*- coding: utf-8 -*-

__author__ = "Kenichi Ohwada"

from server import BaseServer, BaseApplication, BaseHandler

import tornado.ioloop
import tornado.web
from tornado.options import define, options

import os
import glob
import serial
import threading
import logging

# options
define("username")
define("password")
define("serial_port")
define("baudrate", type=int, default=9600)

# constant
APP_NAME = "FabSerial"
SERVER_PORT_DEFAULT = 8010
COOKIE_SECRET = "gaofjawpoer940r34823842398429afadfi4iias"
READ_TIMEOUT = 10
WRITE_TIMEOUT = 600  # 10 min
PARITY = serial.PARITY_NONE
BAUDRATE_TUPLE = (300,600,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200,230400,250000,460800)

# status
STATUS_NONE = 0
STATUS_RUNNING = 1
STATUS_END = 2
STATUS_ERROR = 3

# global variable
g_dir_uploads = ""
g_path_serial = ""
g_path_data = ""
g_error = ""
g_status = STATUS_NONE
g_debug_detail = True

#
# class Server
#
class Server(BaseServer):

    def __init__(self, basedir=None, port=None):
        self.basedir = self.initBasedir(basedir, APP_NAME)
        self.port = self.initServerPort(port, SERVER_PORT_DEFAULT)
        basedir_conf = self.initBasedirSub(self.basedir, "conf")
        self.initBasedirUserConf(basedir_conf)
        # global
        global g_dir_uploads, g_path_serial
        g_dir_uploads = self.initBasedirSub(self.basedir, "uploads")
        g_path_serial = self.initBasedirDeviceConf(basedir_conf, "serial.conf")
        # logging
        self.initLogging(self.basedir, APP_NAME)

    def run(self):
        app = Application()
        app.listen( self.port )
        logging.debug("run on port %d, %s mode" % (self.port, options.logging))
        logging.debug("myself %s, basedir %s" % (self.getSelfDir(), self.basedir))
        tornado.ioloop.IOLoop.instance().start()

#
# class Application
#
class Application(BaseApplication):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/serial_setting", SerialSettingHandler),
            (r"/upload", UploadHandler),
            (r"/excute", ExcuteHandler),
            (r"/status", StatusHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
        ]
        settings = self.getSettings(COOKIE_SECRET)
        tornado.web.Application.__init__(self, handlers, **settings)

#
# class MainHandler
#
class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render(
            "main.html",
            ports = self.getPorts(),
            port_selected = options.serial_port,
            baudrates = BAUDRATE_TUPLE,
            baudrate_selected = options.baudrate,
            filenames = os.listdir( g_dir_uploads ),
            filename_selected = g_path_data
        )

    def getPorts(self):
        ports = []
        ports = ports \
            + glob.glob("/dev/ttyUSB*") \
            + glob.glob("/dev/ttyACM*") \
            + glob.glob("/dev/tty.usb*") \
            + glob.glob("/dev/cu.*") \
            + glob.glob("/dev/cuaU*") \
            + glob.glob("/dev/rfcomm*")
        return ports

#
# class SerialSettingHandler
#
class SerialSettingHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        self.check_xsrf_cookie()
        arg_port = str(self.get_argument("port"))
        arg_baudrate = int(self.get_argument("baudrate"))
        data = "serial_port=\"" + arg_port + "\"\n"
        data += "baudrate=" + str(arg_baudrate) + "\n"
        self.writeFile(g_path_serial, data)
        options.serial_port = arg_port
        options.baudrate = arg_baudrate
        self.redirect("/")

#
# class UploadHandler
#
class UploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        global g_path_data
        self.check_xsrf_cookie()
        name = self.procUpdate( g_dir_uploads )
        if len(name) > 0:
            g_path_data = name
        self.redirect("/")

#
# class ExcuteHandler
#
class ExcuteHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        global g_path_data, g_status, g_error
        self.check_xsrf_cookie()
        g_path_data = str(self.get_argument("filename"))
        g_status = STATUS_NONE
        g_error = ""
        port = options.serial_port
        baudrate = options.baudrate
        self.render(
            "excute.html",
            port = port,
            baudrate = baudrate,
            filename = g_path_data           
            )
        if len(g_path_data) > 0 :
            th = SerialThread( port, baudrate, g_path_data )
            th.start()
        else :
            g_status = STATUS_ERROR
            g_error = "Please select file"

#
# class StatusHandler
#
class StatusHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        json = self.getStatusJson(g_status, g_error)
        logging.debug("StatusHandler:get " + json)
        self.write(json)

#
# class LoginHandler
#
class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        if self.checkLogin(options.username, options.password):
            self.redirect("/")
        else:
            self.redirect("/login")

#
# class LoginHandler
#
class LogoutHandler(BaseHandler):

    def get(self):
        self.clearCurrentUser()
        self.redirect("/")

#
# SerialThread
#
class SerialThread(threading.Thread):

    def __init__( self, port, baudrate, name ):
        super(SerialThread, self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.name = name

    def run(self):
        global g_status, g_error
        g_status = STATUS_RUNNING 
        g_error = "";
        path_data = os.path.join( g_dir_uploads, self.name )
        file_data = None
        ser = None

        try:
            msg = self.port + ", " + str(self.baudrate) + ", " + self.name
            logging.debug("log: " + msg)
            file_data = open(path_data, "r")
            ser = serial.Serial( self.port, self.baudrate, timeout=READ_TIMEOUT, writeTimeout=WRITE_TIMEOUT, parity=PARITY )
            ser.flushOutput()
            for line in file_data:
                ser.write(line)
                if g_debug_detail:
                    logging.debug("> " + line)
            g_status = STATUS_END

        except Exception as e:
            g_status = STATUS_ERROR
            g_error = "Serial Error: " + str(e)
            logging.exception("log: ")

        logging.debug("log: End")
        if file_data is not None:
            file_data.close()
        if ser is not None:
            ser.close()
