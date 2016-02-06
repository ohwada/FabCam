FabCam
===============

Web app to control the machine tools, such as Roland MDX series. <br>

### Requirements
OS: Linux, MacOSX, other UNIX clone
Python 2.7 

### Install
$ git clone https://github.com/ohwada/FabCam.git <br>
$ cd FabCam <br>
$ sudo python setup.py install <br>

you can use service deamon
$ sudo init.sh <br>

### Run
$ /usr/local/bin/fabcam <br>

or service deamon <br>
$ sudo /etc/init.d/fabcam start <br>

### Usage
Access using web browser. <br>
http://localhost:8080 <br>

more detail
https://github.com/ohwada/FabCam/tree/master/docs/ <br/>

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>
