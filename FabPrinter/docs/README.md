FabCam Printer Usage
===============

Web app to control the fab machine, such as Roland SRM series. <br>

### Start
Access using web browser. <br>
http://IP_ADDR:8020 <br>
You can use "localhost" as IP_ADDR, if the app is running on your computer.<br>
You can use hostname such as "fabcam.local" as IP_ADDR, if the app is running with Avahi ( Bonjour clone ).<br>

### Login
Please enter username and password <br>
default username is "fablab", password is "fablab" <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/FabPrinter/docs/fabprinter_login.png" width="300" />

### Setup
(1) Setup printer setting <br>
Please enter "Printer name" that was set in CUPS Manager. <br>
(2) Upload G-code file <br>
(3) Push ”Send" botton <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/FabPrinter/docs/fabprinter_main.png" width="300"/>

### Send to Machine
Usually display immediately "END", and the machine will be run. <br>
If it is taking time to transfer data to the machine, display consecutive dots such as "..." <br>
If the transfer fails, display the reason <br>

<img src="https://raw.githubusercontent.com/ohwada/FabCam/master/FabPrinter/docs/fabprinter_excute.png" width="300"  />

### Notice
This app does not have the generation function of G-code. <br>
Please use fabcam.cc . <br>
http://fabcam.cc/ <br>

### todo
(1) File Management <br>
delete upload files <br>
display log fies <br>
