# -*- coding: utf-8 -*-

__author__ = "Kenichi Ohwada"

from server import BaseServer, BaseApplication, BaseHandler

import tornado.options
from tornado.options import define, options

import os
import subprocess
import threading
import logging

# options
define("username")
define("password")
define("printer")

# command
CMD_LPR = "/usr/bin/lpr"
CMD_HOSTNAME = "/bin/hostname"

# constant
APP_NAME = "FabPrinter"
SERVER_PORT_DEFAULT = 8020
COOKIE_SECRET = "gaofjawpoer940r34823842398429afadfi4iias"

# status
STATUS_NONE = 0
STATUS_RUNNING = 1
STATUS_END = 2
STATUS_ERROR = 3

# global variable
g_dir_uploads = ""
g_path_printer = ""
g_path_data = ""
g_error = ""
g_status = STATUS_NONE

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
        global g_dir_uploads, g_path_printer
        g_dir_uploads = self.initBasedirSub(self.basedir, "uploads")
        g_path_printer = self.initBasedirDeviceConf(basedir_conf, "printer.conf")
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
            (r"/printer_setting", PrinterSettingHandler),
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
            printer = options.printer,
            filenames = os.listdir( g_dir_uploads ),
            filename_selected = g_path_data
        )

#
# class PrinterSettingHandler
#
class PrinterSettingHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        self.check_xsrf_cookie()
        arg_printer = str(self.get_argument("printer"))
        options.printer = arg_printer
        data = "printer=\"%s\"\n" % (arg_printer)
        self.writeFile(g_path_printer, data)
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
        printer = options.printer
        hostname = self.getHostname()
        url = "http://%s.local:631/jobs" % (hostname)
        self.render(
            "excute.html",
            printer = printer,
            filename = g_path_data, 
            url = url          
            )
        if len(g_path_data) > 0 :
            th = PrinterThread( printer, g_path_data )
            th.start()
        else :
            g_status = STATUS_ERROR
            g_error = "Please select file"

    def getHostname(self):
        ret = ""
        try:
            ret  =  subprocess.check_output( CMD_HOSTNAME )
        except Exception as e:
            logging.exception("log: ")
        return ret

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
# PrinterThread
#
class PrinterThread(threading.Thread):

    def __init__( self, printer, name ):
        super(PrinterThread, self).__init__()
        self.printer = printer
        self.name = name

    def run(self):
        global g_status, g_error
        g_status = STATUS_RUNNING 
        g_error = "";
        path_data = os.path.join( g_dir_uploads, self.name )
        cmd = "%s -P %s %s" % (CMD_LPR, self.printer, path_data)

        try:
            logging.debug("log: " + cmd)
            ret  =  subprocess.check_output( cmd.split(" ") )
            logging.debug(ret)
            g_status = STATUS_END

        except Exception as e:
            g_status = STATUS_ERROR
            g_error = "Printer Error: " + str(e)
            logging.exception("log: ")

        logging.debug("log: End")
