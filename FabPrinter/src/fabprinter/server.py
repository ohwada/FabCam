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
import subprocess
import threading
import logging
import logging.config
from datetime import datetime

#
# class BaseServer
#
class BaseServer():

    def __init__():
        pass

    def initBasedir(self, param_basedir, appname):
        if param_basedir is not None:
            basedir = param_basedir
        else:
            basedir = os.path.expanduser(os.path.join("~", "." + appname.lower()))
        if not os.path.isdir(basedir):
            os.makedirs(basedir)
        return basedir

    def initServerPort(self, param_port, default):
        if param_port is not None:
            port = param_port
        else:
            port = default
        return port

    def initBasedirSub(self, basedir, name):
        dir_sub = os.path.join( basedir, name )
        if not os.path.isdir(dir_sub):
            os.makedirs(dir_sub)
        return dir_sub

    def initBasedirUserConf(self, basedir_conf):
        dir_self = self.getSelfDir()
        src_dir_conf = os.path.join( dir_self, "conf" )
        src_path_user = os.path.join( src_dir_conf, "user.conf" )
        dst_path_user = os.path.join( basedir_conf, "user.conf" )
        if not os.path.exists(dst_path_user):
            shutil.copyfile(src_path_user, dst_path_user)
        tornado.options.parse_config_file( dst_path_user )

    def initBasedirDeviceConf(self, basedir_conf, name):
        path = os.path.join( basedir_conf, name )
        if os.path.exists(path):
            tornado.options.parse_config_file(path)
        return path

    def initLogging(self, basedir, appname):
        dir_logs = self.initBasedirSub( basedir, "logs" )
        name_log = appname.lower() + ".log"
        filename = os.path.join(dir_logs, name_log)
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

    def getSelfDir(self):
        return os.path.dirname(__file__)

#
# class BaseApplication
#
class BaseApplication(tornado.web.Application):

    def getSettings(self, cookie_secret):
        settings = dict(
            cookie_secret = cookie_secret,
            static_path = self.getPath( "static" ),
            template_path = self.getPath( "templates" ),
            login_url = "/login",
            xsrf_cookies = True,
            autoescape = "xhtml_escape",
            debug = True,
            )
        return settings

    def getPath(self, name):
        path = os.path.join(os.path.dirname(__file__), name)
        return path

#
# class BaseHandler
#
class BaseHandler(tornado.web.RequestHandler):

    cookie_username = "username"

    # overwrite
    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
#        logging.debug("BaseHandler - username: %s" % username)
        if not username: return None
        return tornado.escape.utf8(username)

    def setCurrentUser(self, username):
        self.set_secure_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clearCurrentUser(self):
        self.clear_cookie(self.cookie_username)

    def checkLogin(self, username, password):
        logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))
        self.check_xsrf_cookie()
        arg_username = self.get_argument("username")
        arg_password = self.get_argument("password")
        logging.debug("LoginHandler:post %s %s" % (arg_username, arg_password))
        if arg_username == username and arg_password == password:
            self.setCurrentUser(username)
            return True
        else:
            return False

    def procUpdate( self, dir_uploads ):
        name, body = self.getUploadFile()
        if (len(name) > 0) and (len(body) > 0):
            filename = os.path.join(dir_uploads, name)
            self.writeFile(filename, body)
        return name

    def getUploadFile(self):
        name = ""
        body = ""
        if self.request.files.has_key("file"):
            files = self.request.files["file"];
            if len(files) > 0 :
                name = str(files[0]["filename"])
                body = str(files[0]["body"])
        return (name, body)

    def writeFile(self, filename, data):
        f = open(filename, "w")
        f.write(data)
        f.close()
        logging.debug("writeFile %s \n%s " % (filename, data))

    def getStatusJson( self, status, error ):
        json = "{\"status\":%d, \"error\":\"%s\"}" %(status, error)
        return json

