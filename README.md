
![CI Pipeline](https://github.com/sagacious-solutions/rgb-everywhere-hardware-api/actions/workflows/python-app.yml/badge.svg)
<a href='https://coveralls.io/github/sagacious-solutions/rgb-everywhere-hardware-api?branch=main'><img src='https://coveralls.io/repos/github/sagacious-solutions/rgb-everywhere-hardware-api/badge.svg?branch=main' alt='Coverage Status' /></a>

# RGB Everywhere Hardware API

This is a repository for lighting device drivers for RGB Everywhere. It allows a raspberry pi to control a WS281x lighting device. An unlimited number of these can be deployed and controlled via the <a href="https://github.com/sagacious-solutions/rgb-everywhere-web-interface">RGB Everywhere Web Interface</a>

# Features

- Continuous Integration via GitHub actions to ensure best possible quality code
- Advanced and visually stunning animations
- Set any device to any color you like
- Save and easily display favorite patterns through the web interface
- Control devices in real time and wow your pets with an ever changing rainbow
- Dance party mode will visualize your spotify tracks into a mesmerizing dance of colors

# Demo of Visualizer

[<img src="https://i.ytimg.com/vi/9jklt9LoFyM/maxresdefault.jpg" width="50%">](https://www.youtube.com/shorts/9jklt9LoFyM "Click for Spotify Visualizer Demo")

Don't be surprised if the whole neighbourhood shows up for the party!

# Tech-Stack

- Raspberry Pi zero 2 W
- GitHub Actions for Continuous Integration Pipeline
- Debian Linux
- Python
- Flask
- python-dotenv
- pytest
- Socket.io
- Audio Analysis from Spotify API
- Binary Search Algorithm for Rapidly Parsing audio data
- ws2811 IC RGB Light Strings and strips
- A Douglas Fir Tree

### To Get Running

1. Install the required libraries `sudo pip install -r requirements.txt`
   - Requirements must be installed as sudo as the service wil run as sudo
2. On the Raspberry Pi, install <a href="https://pm2.keymetrics.io/">PM2</a> to daemonize the HTTP service
   - You will need to install Node JS prior to pm2
   - You can daemonize it anyway you like, if you don't though the service will be lost on reboot
3. Set and forget the service
   - Set the service to run at boot.
   - Make sure the service runs as sudo, otherwise it will error out as it won't have hardware level access

### A note about security

**_If doing this and connecting it online you should understand your network security. I recommend putting the hardware in a VLAN thats firewalled off from the rest of your network or isolating the hardware in your routers DMZ._**

## Hardware

<p>Current hardware is a Raspberry Pi Zero 2 W. A single JST 2 Pin Socket has been soldered to it to connect the lights securely.</p>
<img src="./docs/rpi_zero_2.jpg" width="50%" />

### RGB Lights

This code will work with any ws281x RGB lighting strip thats a single line of LEDs.

<img src="./docs/one_light.jpg" width="50%" />

### Pinout

The RBG signal string is connected to pin12 (GPIO 18) to use the PWM Channel for control. If not using a Raspberry Pi Zero 2 W, you will need to check for a signal channel available on the device you are using.

<img src="./docs/pi_pinout.png" width="50%" />
<p>Image source <a href="https://pinout.xyz/">https://pinout.xyz/</a></p>
