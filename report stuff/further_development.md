# Further Development
The project is not finished, what we have is a test environment that theoretically works, but has not been tested on the actual ground station server. one way to further develop is to take the current system and test it in the context of the MCS

## Testing on the MCS
-   The first thing to do here is to find out how the system interfaces with the API, to do this a lot of digging through github has to be done
-   Connecting a second bluebox to the MCS would be required, here it would be a good idea to contact Nick or Jens about it

## Testing with the satellite in satlab
-   it might be a good idea to send some fec packets to our ground station from the satellite that's set up in satlab
-   maybe try out half duplex
    -   if this works set some requirements for further development of the satellite so it will be compatible with our system
## Fix half duplex with the transmitter bluebox
-   an extensible dive into the transmitter module would have to be done, to see if some mistake happened in translation between full duplex and half duplex
    -   it is only an issue on the satellite's receival, which was a stub anyway so this point might not really be an issue
        -   this is true because the important part is that the satellite is capable of successfully switching the ground station from full duplex to half duplex.
## Implement repeater functionality
-   one way to do this is to append an identifier to the packets such that the satellite knows whether its supposed to repeat the packet or save it internally
-   discuss it with Nick
## Research current encoding more thoroughly now that the deadline is gone
-   With the project handed in, there is less pressure to implement complex goals of the semester and more time to research encoding.
    -   not entirely true since reed-solomon is relevant for algorithms :)

## Half duplex is not finished
-   my personal goal with half duplex is make sure it can do exactly the same as the current system, however there are some features missing
    -   our system is unable to request data from the satellite and switch into a receiver mode until that is done
    -   satellite stub is unable to process requests of specific data
    