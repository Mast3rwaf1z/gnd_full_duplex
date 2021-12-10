
# Design plan
[comment]: # 	(an overall overview of what we have established so far)
[comment]: #	(find out where or if the frequencies have been chosen yet)
[comment]: #	(maybe make an appendix about testing VHF and UHF with blueboxes so we have a scapegoat for only using UHF)
- What does prototype mean for the final verson
## Hardware choices
### an overview of the different solutions that can be used for the design of the GND
- why we're using a rpi
- we could have used a VM
	- issue here might be hardware access so we avoid this one
- we could have built a new x86_64 system
- the two different kinds of blueboxes
### what kind of system are we actually gonna use
- a raspberry pi for simplicity
- two regular blueboxes to accurately show the current system
### an overview of the different solutions that can be used for the design of the satellite
- as the satellite stub is only for testing purposes, its system is irrelevant
- the need for some kind of radio that can send the same protocols as the blueboxes
	- blueboxes
	- a radio module, preferably using the ADF7021 or ADF 7020 to show the compatibility with the satellite



## Software choices
- Choice of programming language? why python makes sense
- why we're not using C for satellite stub
- development tools
	- ipython