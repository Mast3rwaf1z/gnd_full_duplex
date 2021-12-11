note all software developed as part of this project is based on a closed repository under Aalborg University
# AAUSAT ground station
here lies the programs for the full duplex implementation for AAU cubesats
# REQUIREMENTS
- install bbctl: https://github.com/aausat/bbctl
    
    - this will enable the use of the following dependencies like this:
      ```python
      import fec
      import bluebox
      fechandler = fec.PacketHandler(key="key")
      bb = bluebox.Bluebox(frequency=431000000, serial="serial", power=0)
      ```
      you can install this software by issuing the following commands:
      ```console
      $ git clone git@github:aausat/bbctl.git
      $ cd bbctl
      $ pip3 install pyusb --user
      $ pip3 install -r . --user
      ```
- have the hardware used:
- two to four blueboxes
- the full_duplex.py program can run on any system with bbctl installed
- the satelliteStub.py program has only been tested in Arch Linux
    -   The main purpose of this program is to test the capability of the full_duplex.py program
