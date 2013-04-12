django-hautomation
==================

Proyect is at its development stage, not for production yet.

REST API to control home automation deployments coded as Django apps. 

Components
==========

hacore - Django app which holds the core of the system. It has de database definitions.

harest - Django app meant to publish a REST API which accepts the home automation device management and 
the home automation commands.

This proyect can't talk to any home automation device by it self. It needs another modules to understand
how to send commands to the underlining devices. Each module must implement a driver to control a home automation
protocol. For instance, X10 protocol is implemented by the hax10 module and the KNX protocol is implemented by the
haknx module



