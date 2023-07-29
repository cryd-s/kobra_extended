Release Notes
=============

Version
-------
This is release v0.7.2 of the Klipper-dgus_CR6 project.


New at this release
-------------------

The popup keyboard has been repaired. It now displays the numbers as you enter them.
The wrong version of the DGUS Project files were uploaded at release 0.7.1. (Sorry)


Known Issues at this release
----------------------------

1. The DWIN display's memory is not being "reset to zero" when Restart or FWRestart is used. As a result, some fields (like Target Temperatures) may report false information, until the system is made to refresh those values by being used. (e.g. By setting a new target temperature or by starting a print.)
   This issue is also evident after using the Emergency Stop function and then restarting the firmware.
2. Issue 1 can also result in Feed Amount and Feed Rate buttons being green even if they have not been selected, since the firmware was last started.
   Always select the buttons you want activated. Do not assume they are already active, if not pressed since the last restart.
3. The automatic installation script for klipper-dgus is not particularly "robust". If it is cancelled or crashes before completing, for instance, it will abort if you try to run it again.  Unless you can read and understand the logs, you may not realize that script has failed.  If the script fails to autodetect the serial interface to your TTL-USB device, for instance, then perform the Manual Installation instructions, as well.


Installation Instructions
-------------------------

To install this application on a Creality CR6 printer:

1. You must already be using Klipper to operate your CR6 printer.  Instructions for converting your printer from the (Marlin-based) stock Creality or Community Firmware to Klipper are beyond the scope of this documentation.

2. Follow the :ref:`Flash_DWIN_SET_label` instructions in the Installation section of this document.
   - Use the version of DWIN_SET that is in the dgus-project folder of this project; Klipper-dgus_CR6_DWIN_SET_v0.7.zip. 

3. Follow the :ref:`Puthon_App_Installation_instructions_Label` instructions in the Installation section of this document, including the instructions for establishing a serial communications link between your Klipper Host MCU containing Moonraker and your DWIN display. (The use of a TTL-USB adaptor is recommended, for ease of installation, but the GPIO serial interface can also be used.)

4. Verify the installation as follows:

   a. With the printer off:

   Verify that the startup display appears on the screen, with an error message in the text box from Klipper saying that the printer mcu cannot be reached.

   b. With the printer on:

   Verify that the touchscreen operates the interface correctly, as follows:

   - tap the *FWrestart* button on the startup screen, to reboot Klipper and Moonraker
   - confirm that the Overview screen appears on the display
   - select *<* to access the Main Menu screen
   - cycle through each of the screens
   - operate the controls on each screen
   - verify that the data displayed on each screen is correct
   - verify that the Emergency Stop (!) button works on every screen

If you have any troubles with the system not working as described above, please consult the :ref:`Troubleshooting-flashing-problems-label` section of this document for assistance.
If you still have trouble, please review the Issues in the project repository, for similar-sounding problems.

If there is no exising Issue that describes your problem, please open a new Issue and provide enough information for us to be able to understand and reproduce your problem.

Good luck and enjoy!
SPJones, 30Nov2022 
