# IDEAS
to make a reliable system there are a few improvements that can be made for the systems that is gonna use ours, to have a better experience with it
-   make a thread that handles the packets
    -   to make this work efficiently, prepend a byte that specifies if we're requesting some data or if we're sending a file
        -   if we're sending a file, prepend another 2-3 bytes to specify how many packets are coming, the rest of the packets should have their index to avoid mixing of packets
