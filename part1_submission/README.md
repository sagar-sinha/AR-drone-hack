Creators: Christopher Akatsuka, Sagar Sinha, Jeremy Danziger
pennkeys: akatsuka, sagarsi, jdanz

Note: Upon reviewing the submission again, I realized there was a typo on line 20, regarding the ffplay command for the final demo video. This has been fixed in this version, but make command and the mp4 command were still correct before

The entire script exists within the single file.

ffplay, ffmpeg, python, and the python libraries subprocess and scapy are required to run the file
This code was tested in Python 2.7
The file's name is finalhopefullyliveloop.py

In order to run the file, call:

make part1

There is known to be an approximately 4 second lag.

The file creates captured.pcap, a record of the packet capture, and stream.h264, the video file. 

The video you just can be played using the command "make video", or ffplay stream.h264.

The final submission video can be played using the command "make final_video", or ffplay final_demo.h264, or just by opening the mp4 player of your choice.


The mpeg was generate via an online converter with our h264 file

****IMPORTANT*****
In some cases, an error may occur. These may be scapy errors, or an IO error.
In the event of error, rerunning the program is required. 
******************

If you get stuck in monitor mode, call: 

sudo pkill tcpdump 
____________
How it works:
1. Clear preexisitng files
2. Sets the channel
3. Creates general packet capture file (captured.pcap)
4. Continually grab packets over the course of 1 second and filter out non-video packets, while appending new_video frames to the exisiting file (stream.h264).
    a. The video stream opens once the first frame is received, and continues to play with every new second's worth of frames it receives
5. Upon CTRL-C, cleans up the temp files, kills remaining tcpdumps, and exits
____________

Attributions

The below link was used in the beginning from the base code: 
https://thepacketgeek.com/scapy-sniffing-with-custom-actions-part-1/

The below link was used for identifying layers in the packets:
http://null-byte.wonderhowto.com/how-to/build-dns-packet-sniffer-with-scapy-and-python-0163601/

The below link was used for setting the channel:
http://unix.stackexchange.com/questions/48671/how-to-put-mac-os-x-wireless-adapter-in-monitor-mode

The below link was used for determining up the channel, and for using TCP dump with it:
https://supportforums.cisco.com/document/75221/wireless-sniffing-using-mac-os-x-106-and-above
