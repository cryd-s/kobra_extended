.. _Load_Unload_Tutorial_label:

####################
Load/Unload Filament
####################

What you will learn
===================
By following this tutorial, you will learn how to:

- Navigate through the menus
- Park the printhead at the front left corner of the printer
- Tap a displayed value to obtain a popup keyboard
- Use the popup keyboard to enter/modify/cancel or accept a target value
- Heat the nozzle to the desired print temperature
- Select the desired length of filament to load or Unload
- Select the rate at which the Extruder will Load or Unload the filament
- Load filament into the extruder and hotend
- Unload filament from the extruder and hotend 

Additional materials required (optional):
=========================================
- one reel of filament
- one pair of wire snips (to cut a 45 degree tip on the end of the filament)

Tutorial Steps:
===============

1. Power-up the printer, with Klipper and Mainsail already loaded and running

2. Verify that the Overview screen is shown on the DWIN display, with the bed and nozzle temperatures each displayed.

.. figure:: ../../img/tutorials/Load-Unload_Filament/StartAtOverviewMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Example of the Overview Screen 
    
   Before starting this tutorial, verify that the Overview Screen is displayed


3. Tap the "<" symbol at the top left corner of the menu.

.. figure:: ../../img/tutorials/Load-Unload_Filament/NavigateToMainMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Example of the Overview Screen 
    
4. Verify that the Main Menu screen is displayed.

.. figure:: ../../img/tutorials/Load-Unload_Filament/SelectMainMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture of the Main Menu Screen 

5. Tap the "Homing" button

.. figure:: ../../img/tutorials/Load-Unload_Filament/NavigateToHomingMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Highlighting the "Homing" button on the Main Menu Screen 

6. Verify that the Homing menu is displayed.

.. figure:: ../../img/tutorials/Load-Unload_Filament/SelectHomingMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture of the Homing menu 

7. Tap the "Posn 2" button, to park the print head at Position 2, as defined in the klipper-dgus configuration file, "dgus_display_macros.cfg"

.. figure:: ../../img/tutorials/Load-Unload_Filament/SelectParkHead_Position2.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture Highlighting the "Posn 2" button on the Homing menu 

8. Wait for the printer to home X,Y,Z and then to park the head at X=0,Y=0,Z=20.

.. TIP:: The macro codes run by buttons Posn1 and Posn2 are user-programmable.

9. If not already installed, install the filament spool on the printer.
10. If not already cut at 45 degrees, cut the end of the filament at a 45 degree angle.

.. Figure:: ../../img/tutorials/Load-Unload_Filament/45DegTip.JPG
   :scale: 20
   :align: center
   :alt: Picture of filament with 45 degree tip cut at end

11. Feed the filament into the extruder, and up to the point where it meets resistance (i.e. at the point where the extruder will grab the filament and feed it forward, when "Load" is selected.).
12. Return to the Main Menu screen.
13. Tap the "Extruder" button, to navigate to the Extruder menu.

.. figure:: ../../img/tutorials/Load-Unload_Filament/NavigateToExtruderMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture Highlighting the "Extruder" button on the Main menu 


14. Verify that the Extruder menu is displayed.

.. figure:: ../../img/tutorials/Load-Unload_Filament/SelectExtruderMenu.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture of the Extruder menu screen

15. Tap the "nozzle target temperature" field.

.. figure:: ../../img/tutorials/Load-Unload_Filament/TapTargetValue.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture highlighting the field to tap + the popup keyboard

16. Verify that a keyboard pops up.
17. Type in an appropriate printing temperature for the filament you will load (e.g. 240, for PeTG) and tap the big green checkmark to Enter that value.

.. figure:: ../../img/tutorials/Load-Unload_Filament/LoadTemperatureSet.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture highlighting the field to tap + the popup keyboard

18. Tap the 50mm Feed Amount button. Note that it is green and all of the other buttons are grey. 
    (Optionally) Experiment with pushing the other Feed Amount buttons, to see what happens.

.. figure:: ../../img/tutorials/Load-Unload_Filament/SetEExtrusionLength.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture highlighting the 50mm Extruder Feed Amount button 

19. Tap the 15mm/sec Feed Rate button.
    (Optionally) Experiment with pushing the other Feed Rate buttons, to see what happens.

.. figure:: ../../img/tutorials/Load-Unload_Filament/SetEExtrusionRate.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture highlighting the 15mm/sec Extruder Feed Rate button

20. When the nozzle temperature reaches the target value, press the "Load" button.  
    Note that the extruder loads 50mm of filament at the chosen Feed Rate.
    (Tip: You may have to Load 50mm several times, before you see filament come out of the nozzle.)

.. figure:: ../../img/tutorials/Load-Unload_Filament/SelectLoad.JPG
   :height: 400
   :width: 272
   :scale: 100
   :align: center
   :alt: Picture highlighting the 15mm/sec Extruder Feed Rate button

21. Optionally, experiment with Loading filament at different Feed Rates. 
    (TIP: If your extruder makes "crack" noises and visibly struggles at the highest Feed Rate, you may find this experiment reveals a better value to use in practice.)

22. Based on what you learned following steps 1-20, now *Unload* the filament.