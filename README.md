# cheerymqtt
This program watches the CheerLights (http://cheerlights.com/) feed
and publishes messages to an MQTT broker. Quick hack, might break.
Partly based on code from https://github.com/snorecore/MincePi

Defaults to publishing to "spooplights" and "spooplightsRGB" topics
on iot.eclipse.org, but you should probably change this to something
else. The connection code isn't very robust, and if the code can't get
the colour it'll default to black.

Requires paho-mqtt and request packages.
