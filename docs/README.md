FabCam Usage
===============

Web app to control the machine tools, such as Roland MDX series. <br>

### Start
Access using web browser. <br>
http://IP_ADDR:8080 <br>
You can use "localhost" as IP_ADDR, if the app is running on your computer.<br>
You can use hostname such as "fabcam.local" as IP_ADDR, if the app is running with Avahi ( Bonjour clone ).<br>

### Login
Please enter username and password <br>
default username is "fablab", password is "fablab" <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/docs/fabcam_login.png" width="300" />

### Setup
(1) Setup serial setting <br>
If Serial Port is empty, connect the machine with USB cable, and refresh web brawser.
(2) Upload G-code file <br>
(3) Push ”Excute" botton <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/docs/fabcam_main.png" width="300"/>

### Excute
Usually display immediately "END", and the machine will be run. <br>
If it is taking time to transfer data to the machine, display consecutive dots such as "..." <br>
If the transfer fails, display the reason <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/docs/fabcam_excute.png" width="300"  />

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>

### todo
(1) File Management <br>
delete upload files <br>
display log fies <br>

(2) Python Virtual Environments <br>
