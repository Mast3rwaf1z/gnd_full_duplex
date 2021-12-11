Note all software developed as part of this project is based on a closed repository under Aalborg University
# AAUSAT ground station
Here lies the programs for the full duplex implementation for AAU cubesats
## REQUIREMENTS
- Install bbctl: https://github.com/aausat/bbctl
    
    - This will enable the use of the following dependencies like this:
      ```python
      import fec
      import bluebox
      fechandler = fec.PacketHandler(key="key")
      bb = bluebox.Bluebox(frequency=431000000, serial="serial", power=0)
      ```
      You can install this software by issuing the following commands:
      ```console
      $ git clone git@github:aausat/bbctl.git
      $ cd bbctl
      $ pip3 install pyusb --user
      $ pip3 install -r . --user
      ```
- Have the hardware used:
- Two to four blueboxes
- The full_duplex.py program can run on any system with bbctl installed
- The satellite_stub.py program has only been tested in Arch Linux
    -   The main purpose of this program is to test the capability of the full_duplex.py program
