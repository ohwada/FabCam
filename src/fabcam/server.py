# -*- coding: utf-8 -*-

__author__ = "Kenichi Ohwada"

import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.options
from tornado.options import define, options

import os
import glob
import shutil
import serial
import threading
import logging
import logging.config
from datetime import datetime

# options
define("username")
define("password")
define("serial_port")
define("baudrate", type=int, default=9600)

# constant
APPNAME = "FabCam"
COOKIE_SECRET = "gaofjawpoer940r34823842398429afadfi4iias"
READ_TIMEOUT = 10
WRITE_TIMEOUT = 600  # 10 min
PARITY = serial.PARITY_NONE
BAUDRATE_TUPLE = (300,600,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200,23040,250000)

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
class Server():

    def __init__(self, basedir=None, port=8080):
        # basedir
        self.init_basedir(basedir)

        # port
        if port is not None:
            self.port = port
        else:
            self.port = 8080

        self.dir_logs = os.path.join( self.basedir, "logs" )
        self.dir_self = os.path.dirname(__file__)
        dir_conf_src = os.path.join( self.dir_self, "conf" )
        path_user_src = os.path.join( dir_conf_src, "user.conf" )
        basedir_conf = os.path.join( self.basedir, "conf" )
        self.path_user = os.path.join( basedir_conf, "user.conf" )

        # global
        global g_dir_uploads, g_path_serial
        g_dir_uploads = os.path.join( self.basedir, "uploads" )
        g_path_serial = os.path.join( basedir_conf, "serial.conf" )

        # makedirs
        if not os.path.isdir(self.dir_logs):
            os.makedirs(self.dir_logs)

        if not os.path.isdir(g_dir_uploads):
            os.makedirs(g_dir_uploads)

        if not os.path.isdir(basedir_conf):
            os.makedirs(basedir_conf)

        # copyfile
        if not os.path.exists(self.path_user):
            shutil.copyfile(path_user_src, self.path_user)

    def run(self):
        tornado.options.parse_config_file( self.path_user )
        if os.path.exists(g_path_serial):
            tornado.options.parse_config_file( g_path_serial )
        app = Application()
        app.listen( self.port )
        self.init_logging()
        logging.debug('run on port %d, %s mode' % (self.port, options.logging))
        logging.debug('myself %s, basedir %s' % (self.dir_self, self.basedir))
        tornado.ioloop.IOLoop.instance().start()

    def init_basedir(self, basedir):
        if basedir is not None:
            self.basedir = basedir
        else:
            self.basedir = os.path.expanduser(os.path.join("~", "." + APPNAME.lower()))

        if not os.path.isdir(self.basedir):
            os.makedirs(self.basedir)

    def init_logging(self):
        filename = os.path.join(self.dir_logs, "fabcam.log")
        config = {
            "version": 1,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "simple",
                    "when": "D",
                    "backupCount": "1",
                    "filename": filename
                },
            },
            "loggers": {
                "tornado.application": {
                    "level": "INFO"
                },
                "tornado.general": {
                    "level": "INFO"
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console", "file"]
            }
        }
        logging.config.dictConfig(config)
        logging.captureWarnings(True)

#
# class Application
#
class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/serial_setting', SerialSettingHandler),
            (r'/upload', UploadHandler),
            (r'/excute', ExcuteHandler),
            (r'/status', StatusHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
        ]
        settings = dict(
            cookie_secret = COOKIE_SECRET,
            static_path = self.getPath( "static" ),
            template_path = self.getPath( "templates" ),
            login_url = "/login",
            xsrf_cookies = True,
            autoescape = "xhtml_escape",
            debug = True,
            )
        tornado.web.Application.__init__(self, handlers, **settings)

    def getPath(self, name):
        path = os.path.join(os.path.dirname(__file__), name)
        return path

#
# class BaseHandler
#
class BaseHandler(tornado.web.RequestHandler):

    cookie_username = "username"

    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
#        logging.debug('BaseHandler - username: %s' % username)
        if not username: return None
        return tornado.escape.utf8(username)

    def set_current_user(self, username):
        self.set_secure_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)

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
        port = str(self.get_argument("port"))
        baudrate = int(self.get_argument("baudrate"))
        self.write(port, baudrate)
        options.serial_port = port
        options.baudrate = baudrate
        self.redirect("/")

    def write(self, port, baudrate):
        data = "serial_port=\"" + port + "\"\n"
        data += "baudrate=" + str(baudrate) + "\n"
        f = open(g_path_serial, "w")
        f.write(data)
        f.close()
        logging.debug("SerialSettingHandler:write %s \n%s " % (g_path_serial, data))

#
# class UploadHandler
#
class UploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        global g_path_data
        self.check_xsrf_cookie()
        name, body = self.getFile()
        if (len(name) > 0) and (len(body) > 0):
            g_path_data = name
            self.writeFile(name, body)

        self.redirect("/")

    def getFile(self):
        name = ""
        body = ""
        if self.request.files.has_key("file"):
            files = self.request.files["file"];
            if len(files) > 0 :
                name = str(files[0]["filename"])
                body = str(files[0]["body"])

        return (name, body)
 
    def writeFile(self, name, body):
        filename = os.path.join( g_dir_uploads, name )
        f = open(filename, "w")
        f.write(body)
        f.close()
        logging.debug('UploadHandler:wite: %s ' % (filename))

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
        global g_status
        data = "{\"status\":" + str(g_status) + ", \"error\":\"" + g_error + "\"}"
#        logging.debug("StatusHandler:get " + data)
        self.write(data)

#
# class LoginHandler
#
class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))
        self.check_xsrf_cookie()
        username = self.get_argument("username")
        password = self.get_argument("password")
        logging.debug('LoginHandler:post %s %s' % (username, password))

        if username == options.username and password == options.password:
            self.set_current_user(username)
            self.redirect("/")
        else:
            self.redirect("/login")

#
# class LoginHandler
#
class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_current_user()
        self.redirect('/')

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
            logging.debug('log: ' + msg)
            file_data = open(path_data, "r")
            ser = serial.Serial( self.port, self.baudrate, timeout=READ_TIMEOUT, writeTimeout=WRITE_TIMEOUT, parity=PARITY )
            ser.flushOutput()
            for line in file_data:
                ser.write(line)
                if g_debug_detail:
                    logging.debug("> " + line)

            g_status = STATUS_END

        except OSError as e:
            g_status = STATUS_ERROR
            g_error = "Serial Error: " + e.strerror
            logging.exception('log: ')

        except serial.SerialException as e:
            g_status = STATUS_ERROR
            g_error = "Serial Error: " + str(e)
            logging.exception('log: ')

        except Exception as e:
            g_status = STATUS_ERROR
            g_error = "Serial Error: " + str(e)
            logging.exception('log: ')

        logging.debug('log: End')
        if file_data is not None:
            file_data.close()
        if ser is not None:
            ser.close()
