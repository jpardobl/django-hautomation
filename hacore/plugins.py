# place to initialize protocol plugins
# plugins must have a start_up function: <module>.start_up()
import logging
from models import Protocol
#import simplejson
from ginsfsm.gobj import GObj
from ginsfsm.gaplic import GAplic, setup_gaplic_thread

#logging.basicConfig(level=logging.DEBUG)

# initialize plugin threads
# --------------------------

drivers = []
try:
    protocols = Protocol.objects.all()
    for protocol in protocols:
        logging.debug("loading %s protocol driver..." % protocol.name)
        exec "from %s import start_up" % protocol.module

        drivers.append(start_up())
except Exception:
    pass


# initialize plugins controller
# -----------------------------
def ac_rx_tx_data(self, event):
    data = event.kw['data']
    logging.debug("RECIBO======> %s" % data)
    self.broadcast_event('EV_DEVICE_UPDATE', data=data)


def ac_rx_tx_error(self, event):
    data = event.kw["data"]
    logging.debug("RECIBO ERROR======> %s" % data)
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
        try:

            for protocol in protocols:
                driver = global_get_gobj(protocol.gobj_name)
                driver.subscribe_event(
                    ['EV_DEVICE_UPDATE', 'EV_ERROR'],
                    self,
                )
        except Exception:
            pass

local_conf = {
    'router_enabled':  True,
    'GRouter.server':  True,
    'GRouter.localhost_route_ports':  8002,
    'GRouter.trace_router':  False,
    'GObj.trace_mach':  False,
    'GObj.trace_creation':  False,
    'GObj.trace_traverse':  False,
    'GObj.trace_subscription':  False,
    'GSock.trace_dump':  False,
    'GObj.logger': logging,

}

ga_controller = GAplic(name='plugin_controller_gaplic', roles='hautomation', **local_conf)
controller = ga_controller.create_gobj(
    'plugin_controller',
    Controller,
    ga_controller,
    __unique_name__=True,
)

thread_controller = setup_gaplic_thread(ga_controller)
thread_controller.start()
