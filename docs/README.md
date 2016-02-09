FabCam Usage
===============

Web app to control the machine tools, such as Roland MDX series. <br>

### Start
Access using web browser. <br>
http://IP_ADDR:8080 <br>
You can use "localhost" as IP_ADDR, if the app is running on your computer.<br>
You can use hostname such as "fabcam.local" as IP_ADDR, if the app is running with Avahi ( Bonjour clone ).<br>

### Login
Please enter username and password
default username is "fablab", password is "fablab"

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/docs/fabcam_login.png" width="200"  />

### Setup
(1) Setup serial setting
If Serial Port is empty, connect the machine with USB cable, and refresh web brawser.
(2) Upload G-code file
(3) Push ”Excute" botton

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/docs/fabcam_main.png" width="200"  />

### Excute
Usually display immediately "END", and the machine will be run.
If it is taking time to transfer data to the machine, display consecutive dots such as "..."
If the transfer fails, display the reason

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/docs/fabcam_excute.png" width="200"  />

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>

### todo
(1) File Management
delete upload files
display log fies

(2) Python Virtual Environments

