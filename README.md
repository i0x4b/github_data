just a basic project that uses rabbitmq to send commands every which way.

when main.py runs in master mode, the master will start sending commands to download/read files to the rabbitmq
queue, which is then processed by everything running in "processor" mode. meant to be used as a POC
for containers and just to have fun with python!