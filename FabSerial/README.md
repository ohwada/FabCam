FabCam Serial
===============

Web app to control the fab machine, such as Roland MDX series. <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/FabSerial/docs/fabserial_main.png" width="200"/>

### Requirements
- OS: Raspbian (Debian for Rapsberry Pi), other UNIX clone <br>
- Python 2.7 <br>
- [Virtualenv](https://virtualenv.readthedocs.org/en/latest/) <br>

### Install
$ cd ~<br>
$ git clone https://github.com/ohwada/FabCam.git <br>
$ cd FabCam <br>
$ virtualenv venv <br>
$ source venv/bin/activate <br>
(venv) $ cd FabSerial <br>
(venv) $ python setup.py install <br>
$ deactivate <br>

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
https://github.com/ohwada/FabCam/tree/master/FabSerial/docs/ <br>

### Compatible models
- Milling: Roland MDX-15 (baudrate 9600)
- LaserCutter: Trotec Speedy 100 (baudrate 19200)

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>
http://fabcam.cc/ <br>
