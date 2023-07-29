*************
Display Masks
*************

.. uml::

    (*) --> Startup
    note right
    When Display is powered on,
    or klipper is in any other state
    then ready. This mask will be 
    automatically shown.

    Features:
    -Restart
    -FW Restart
    end note

    Startup --> MainMenu
    note right
    Central Menu to reach
    all functions
    end note

    MainMenu --> Overview
    note bottom
    This mask will be automatically shown
    when klippy enters ready state.

    Features:
    - Control Bed, Extruder Temperature
    - Show Printtime and progress
    - Show actual postion of printhead
    - Pause* / Resume* / Cancel Print*
      (*these only work when "printing")
    end note

    MainMenu --> Homing
    note bottom
    Features:
    - Homing
    - Drive Axes
    - Perform Z-Tilt
    - 2 user def. postions
    end note

    MainMenu --> Extruder
    note bottom
    Features:
    - Extrude
      Retract
      Filament
    end note

    MainMenu --> Tuning
    note bottom
    Features:
    -Set Z-Offset
    -Set SpeedFactor
    -Set ExtrusionFactor
    end note


    MainMenu --> Fan-LED
    note bottom
    Features:
    -Control Extruder FAN
    -Switch LED
    end note


.. toctree::
      :maxdepth: 1
      :caption: Display Masks:

      display_masks/overview_mask
      display_masks/homing_mask
      display_masks/extruder_mask
      display_masks/tuning_mask
      display_masks/fan_mask
      