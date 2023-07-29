.. _display-control-application-communication:

Display Application Communication
=================================
The Display Control Application creates the link between Klipper and the DGUS Display, using the Moonraker JSON RPC API.

.. uml::

    Moonraker <--> "Display Control Application" : Websocket\n(JSON-RPC)
    "Display Control Application" <--> "DGUS Display" : Serial Interface\n(python-dgus)
