General
=======

This project modifies and extends the klipper-dgus solution published and maintained by Sebastian Holzgreve at https://github.com/seho85/klipper-dgus.

Sebastian's klipper-dgus project provides users of the `Anycubic Vyper 3D printer <https://www.anycubic.com/products/anycubic-vyper>`_ with:
   1. A python application that enables a DGUS Display application to interact with `Klipper3D <https://www.klipper3d.org/>`_, through two serial interfaces:
       a. a python-dgus serial communications interface, exploiting `his python-dgus library <https://github.com/seho85/python-dgus>`_, and
       b. a python-moonraker serial communications interface, exploiting `the Moonraker API <https://moonraker.readthedocs.io/en/latest/web_api/>`_
   2. A DGUS application developed with the DGUSTool 8.2.1.14 to work with the *DMG80480C043_02WTRZ07* from DWIN, which is the stock Vyper TFT display.
   3. Documentation designed to help users with Installation, Development and Troubleshooting of klipper-dgus.

This project provides an alternative DGUS application, paired with the same two klipper-dgus serial communication interfaces and the same python-dgus library as the Vyper project.
The DGUS application in this project works with the 272x480 pixel DWIN display provided stock with the Creality CR6-SE and CR6-MAX printers.

The initial set of screens bundled with this project were rescaled from the klipper-dgus Vyper DGUS application and modified, to:
   - remove the Z-Tilt function, which is not available on the CR6
   - remove slider controls, which did not operate satisfactorily
   - rearrange some controls and data displays, for aesthetic reasons

This project documentation is an adaptation and extension of the documentation provided with klipper-dgus, tailored to document this Klipper-dgus_CR6 project.

The latest release of klipper-dgus_CR6 DWIN_SET can be downloaded from `here <https://github.com/Thinkersbluff/Klipper-dgus_CR6/releases>`_
Prior releases are also available, there, each with the matching version of this evolving documentation.

.. warning:: 
    This project is still under development.
    It may not all work as expected or described.

    Please feel to create an Issue on the project GitHub <https://github.com/Thinkersbluff/Klipper-dgus_CR6>, if you encounter problems.