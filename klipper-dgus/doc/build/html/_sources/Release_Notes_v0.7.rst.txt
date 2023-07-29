Release Notes
=============

The first functional release of the Klipper-dgus_CR6 project is v0.7.

The screens and functionality approximate those of the Klipper-dgus_Vyper DGUS application, with the following minor changes:

1. The Z-Tilt function was removed, since that functionality is not available on the CR6.
2. The slider controls were removed, since they did not operate correctly with touch on the 272x480 screen.
3. Some control names were changed and some were rearranged, for aesthetic reasons.

To install this application on a Creality CR6 printer:

1. You must already be using Klipper to operate your CR6 printer.  Instructions for converting your printer from the (Marlin-based) stock Creality or Community Firmware to Klipper are beyond the scope of this documentation.
2. Follow the klipper-dgus installation instructions in the Installation section of this document, including the instructions for establishing a serial communications link between your Klipper Host MCU containing Moonraker and your DWIN display. (The use of a TTL-USB adaptor is recommended, for ease of installation, but the GPIO serial interface can also be used.)
3. Download Klipper-dgus_CR6_DWIN_SET_v0.7.zip. 
4. Extract and copy the DWIN_SET folder to an empty SD card (FAT32, 4096 sectors)
5. Flash the DWIN_SET to your CR6 DWIN display.
6. With the printer off:
Verify that the startup display appears on the screen, with an error message in the text box from Klipper saying that the printer mcu cannot be reached. 
7. With the printer on:
Verify that the touchscreen operates the interface correctly:
- tap the "FWrestart" button on the startup screen, to reboot Klipper and Moonraker
- confirm that the Overview screen appears on the display
- select "<" to access the Main Menu screen
- cycle through each of the screens
   - operate the controls on each screen
   - verify that the data displayed on each screen is correct
   - verify that the Emergency Stop (!) button works on every screen

If you have any troubles with the system not working as described above, please consult the Troubleshooting section of this document for assistance.
If you still have trouble, please review the Issues for similar-sounding problems.
If there is no exising Issue that describes your problem, please open a new Issue and provide enough information for us to be able to understand and reproduce your problem.

Good luck and enjoy!
SPJones, 19Nov2022 