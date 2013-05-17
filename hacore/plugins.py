# place to initialize protocol plugins
# plugins must have a start_up function: <module>.start_up()
import logging
from models import Protocol
import simplejson
from ginsfsm.gobj import GObj
from ginsfsm.gaplic import GAplic, setup_gaplic_thread

logging.basicConfig(level=logging.DEBUG)

# initialize plugin threads
# --------------------------

drivers = []
protocols = Protocol.objects.all()
for protocol in protocols:
    print "loading %s protocol driver..." % protocol.name
    exec "from %s import start_up" % protocol.module

    drivers.append(start_up())


# initialize plugins controller
# -----------------------------

def ac_rx_tx_data(self, event):
    data = event.kw['data']
    print("RECIBO======> %s" % data)
    self.broadcast_event('EV_DEVICE_UPDATE', data=data)


def ac_rx_tx_error(self, event):
    data = event.kw["data"]
    print("RECIBO ERROR======> %s" % data)
    self.broadcast_event('EV_ERROR', data=data)


CONTROLLER_FSM = {
    'event_list': (
        'EV_DEVICE_UPDATE:bottom input top output',
        'EV_COMMAND:bottom output',
        'EV_ERROR: bottom input top output',

    ),
    'state_list': ('ST_IDLE',),
    'machine': {
        'ST_IDLE':
        (
            ('EV_DEVICE_UPDATE',      ac_rx_tx_data,     'ST_IDLE'),
            ('EV_ERROR', ac_rx_tx_error, 'ST_IDLE'),

        ),
    }
}

CONTROLLER_CONFIG = {}


class Controller(GObj):
    """  Driver1 GObj.

    .. ginsfsm::
       :fsm: CONTROLLER_FSM
       :config: CONTROLLER_CONFIG


    *Input-Events:*

        * :attr:`'EV_DEVICE_UPDATE'`: Receiving data.
            Receiving data from urls.

    *Output-Events:*
    8
        * :attr:`'EV_COMMAND'`: Sending command to device.
           Sending command to devices
        * :attr:`'EV_DEVICE_CHANGED'`: Sending device change to external modules
           Sending device change to external modules

    """
    def __init__(self):
        GObj.__init__(self, CONTROLLER_FSM, CONTROLLER_CONFIG)

    def start_up(self):
        """ Initialization zone."""
        from ginsfsm.globals import global_get_gobj

        driver_x10 = global_get_gobj("driver_X10")
        driver_x10.subscribe_event(
            ['EV_DEVICE_UPDATE', 'EV_ERROR'],
            driver_x10,
        )


local_conf = {
    'GObj.trace_mach': True,
    'GObj.logger': logging,
}

local_conf = {
    'router_enabled':  True,
    'GRouter.server':  True,
    'GRouter.localhost_route_ports':  8002,
    'GRouter.trace_router':  True,
    'GObj.trace_mach':  True,
    'GObj.trace_creation':  False,
    'GObj.trace_traverse':  True,
    'GObj.trace_subscription':  True,
    'GSock.trace_dump':  True,
    'GObj.logger': logging,
}

ga_controller = GAplic(name='plugin_controller_gaplic', roles='controller', **local_conf)
controller = ga_controller.create_gobj(
    'plugin_controller',
    Controller,
    ga_controller,
    __unique_name__=True,
)

thread_controller = setup_gaplic_thread(ga_controller)
thread_controller.start()
