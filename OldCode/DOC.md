STEMbot Documentation
====================

Contents
--------

* pi-driver - Starts the motor driver.
* ps3-driver - Starts the controller.
* reset-cam - Restarts the camera driver.

Usage
-----

Start the controller:

    sixad -s
    python ps3-driver.py

Start the thrusters:

    ssh pi@raspberrypi
    raspberry
    sudo python pi-driver.py
    
View the video feed:
* Navigate to [http://raspberrypi:8080](http://raspberrypi:8080).
* Click the WebRTC link.
* Click start.

Troubleshooting
---------------

If there's trouble with the camera:

    ./reset-camera

Installation
------------

**Controls**

    git clone https://github.com/osu-uwrt/stembot.git

**Camera:**

    curl http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc | sudo apt-key add -
    deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ wheezy main
    sudo apt-get update
    sudo apt-get install uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-webrtc

* Source: [Linux Projects](http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14)
