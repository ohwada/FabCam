FabCam Serial
===============

Web app to control the fab machine, such as Roland MDX series. <br>

### Requirements
- OS: Linux, MacOSX, other UNIX clone <br>
- Python 2.7 <br>
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/)

### Install
$ cd ~<br>
$ git clone https://github.com/ohwada/FabCam.git <br>
$ cd FabCam<br>
$ virtualenv venv
$ source venv/bin/activate
(venv) $ cd FabSerial
(venv) $ python setup.py install <br>
$ deactivate

you can use service deamon <br>
$ sudo sh init.sh <br>

### Run
$ cd ~<br>
$ FabCam/venv/bin/fabserial <br>

or service deamon <br>
$ sudo /etc/init.d/fabserial start <br>

### Usage
Access using web browser. <br>
http://localhost:8010 <br>

more detail <br>
https://github.com/ohwada/FabCam/tree/master/FabSerial/docs/ <br/>

### Compatible models
- Milling: Roland MDX-15 (baudrate 9600)
- LaserCutter: Trotec Speedy 100 (baudrate 19200)

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>
http://fabcam.cc/ <br>
