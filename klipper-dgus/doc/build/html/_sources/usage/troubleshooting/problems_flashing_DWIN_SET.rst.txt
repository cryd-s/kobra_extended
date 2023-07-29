.. _Troubleshooting-flashing-problems-label:

Problems Flashing DWIN_SET
==========================

First, let's review the contents of the DWIN_SET folder, so that you have some idea of what it does.

That should also give you some idea what the bluescreen is showing you, as you flash it.


The Contents of DWIN_SET
------------------------
   The DWIN_SET folder in this distribution contains the following files:

1. The Menu Screen Background BitMap Files
   
   All of the files whose name ends in ".bmp" are bitmap files used as the background graphics, one for each screen in the application.
   The screen bitmaps are actually flashed to the display from the 32.icl file, not from these .bmp files. The .bmps are included in DWIN_SET folder purely so that the developer can see the bitmap screen for reference, when working in the DGUSTool to place control and display overlays in the right place on each screen.

   It is ok, but not necessary, to delete the .bmp files from your copy of DWIN_SET.

2. The T5L display configuration file T5LCFG_272480K.configuration

   Flashing the T5L configuration file to the DWIN display programs the display with key behaviours.
   It is only necessary to flash this file once to the DWIN display.  You can (optionally) remove it after that, to speed up the flashing process.

   The CFG file can be opened, modified, and saved, using the DGUSTool tool-config CFG tool.

   .. figure:: ../../img/tool-cfg_menu.jpg
      :scale: 50%

   .. figure:: ../../img/BuildT5LCFG.jpg 
      :scale: 50%

   .. Warning:: You can actually "brick" your DWIN display, if you make incorrect settings in the T5L file.

3. The DGUS application .BIN files

   The files 22_Config.bin, 13ShowFile.bin and 14TouchFile.bin flash the application instructions to the display.

4. The DGUS application .ICL files

   The files 32.icl and 40.icl flash the DGUS application graphics to the DWIN display.

.. NOTE:: The file 42.icl contains a slider knob graphic which is not used at version 0.7.0 of this application. You may (optionally) ignore or remove that file from your copy of DWIN_SET.

5. The DGUS application FONT file

   The file 0_DWIN_ASC.HZK flashes the system font B612mono to the display. This is the same font used with the CR6Community Firmware. It is modified to replace the \` character with the degrees symbol, to label temperature values. 
   
   This file only needs to be flashed to the dsiplay once. 
   It is slow to load and you can deleted it from DWIN_SET, once it has been successfully flashed.
   If you previously flashed the CR6Community Firmware to your display, you should not need to flash this font file again, when flashing this klipper-dgus application.


See :ref:`DWIN_SET_Config_Files_label` for more information about the above files.


What Could Possibly Go Wrong?
-----------------------------

The DWIN display is "notoriously picky" about the partitioning and formatting of the micro SD card used to flash DWIN_SET.

If the bootloader program encounters problems reading the card, it does not throw any error messages, it just "hangs."

When it hangs, you may see a blank (backlit) screen or you may see the blue screen with some or none of the expected text, but the screen may freeze before the flash process completes.

If the bootloader cannot read the files on the card, you may see all "000,s" displayed as the number of files loaded.


What Can You Try?
-----------------

The advice for dealing with any or all of the above symptoms is the same:

1. Make sure that the card is partitioned as MBR (Master Boot Record), DOS if using a MAC. It must NOT be partitioned as GPT.
2. Make sure that the first Primary Partition on that card is formatted FAT32, with 4096 allocation units per sector.  (TIP: A GPT disk will show "Healthy Partition", not "Primary Partition")
3. Perform a full format (not quick format) of the card, to repair or "cordon-off" any broken sectors.
4. Put an EMPTY folder named DWIN_SET on the card
5. With Power OFF: Put the card into the display
6. Switch Power ON the display and verify that the blue screen shows which DGUS2 OS is loaded in the display, 000's for each type  of file and END! at the end of the second line when the process is finished. 
7. If step 6 works, then try again to flash with just the T5LCFG file added to DWIN_SET.
   If step 6 fails, use a new SD card from a respected manufacturer
8. If step 7 works, then try again to flash the other DWIN_SET files.

.. NOTE:: Unlike the CR6Community Firmware, it should not matter which DGUS2 OS is on your display. This application is coded with DGUSTool 8.2.1.14; the same tool used to build the refactored CR6Community Firmware.
