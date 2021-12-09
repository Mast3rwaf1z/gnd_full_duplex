# Implementation plan
The plan for this chapter is to have a 
## full duplex design
-   Two bluebox micros connected only to USB
-   A raspberry pi 4 running armv7 Arch Linux ARM and has bbctl installed
## What is bbctl
-   Software designed to interface with bluebox transceivers
-   Features?
    -   command line encoding
        -   fec integrated
    -   python interface
## Half duplex compatibility design
-   A handler for when a satellite radio "dies"
    -   we'll call this bbcheck, it is part of the satellite_stub program
## Test prep
-   GUI
    -   queue button
    -   text field to send plain text packets
    -   