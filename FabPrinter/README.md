FabCam Printer
===============

Web app to control the fab machine, such as Roland SRM series. <br>

### Requirements
- OS: Linux, MacOSX, other UNIX clone <br>
- CUPS (Common Unix Printing System) <br>
- Python 2.7 <br>
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/)

### Install
$ cd ~<br>
$ git clone https://github.com/ohwada/FabCam.git <br>
$ cd FabCam<br>
$ virtualenv venv
$ source venv/bin/activate
(venv) $ cd FabPrinter
(venv) $ python setup.py install <br>
$ deactivate

you can use service deamon <br>
$ sudo sh init.sh <br>

### Run
$ cd ~<br>
$ FabCam/venv/bin/fabprinter <br>

or service deamon <br>
$ sudo /etc/init.d/fabprinter start <br>

### Usage
Access using web browser. <br>
http://localhost:8020 <br>

more detail <br>
https://github.com/ohwada/FabCam/tree/master/FabPrinter/docs/ <br/>

### Compatible models
- Milling: Roland SRM-20
- LaserCutter: Epilog Helix

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>
http://fabcam.cc/ <br>
