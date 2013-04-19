"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
#from django.test import TestCase
from django.core.urlresolvers import reverse
import requests
import os
from hacore.models import Protocol
from django.conf import settings


def show_response(response):
    print "Return code: %s\nContent: %s\n" % (response.status_code, response.content)


def populate_initial_data():
    Protocol(name="X10", module="hautomation_x10.cmds", validate_address_module="hautomation_x10.utils").save()


def new_device(protocol, did, device_type, url):
    data = {
            "caption": "created automatic",
            "did": did,
            "device_type": device_type,
            "protocol": protocol,
        }
    return requests.post("%s%s" % (url, reverse("device")), data=data)


def del_device(did, url):
    return requests.delete("%s%s" % (url, reverse("device_by_id", kwargs={"did": did})))


class RestTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(RestTest, cls).setUpClass()

        #Protocol(name="KXN", ").save()

        try:
            if settings.TEST_SERVER is not None and settings.TEST_SERVER != "":
                cls.live_server_url = settings.TEST_SERVER
            else:
                populate_initial_data()
        except AttributeError:
            populate_initial_data()


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(RestTest, cls).tearDownClass()


class DeviceTest(RestTest):

    def test_post(self):
        print "Running DeviceTest.post(create)....................................."
        data = {
            "caption": "Persiana terraza",
            "did": "A1",
            "device_type": "dimmer",
            "protocol": "saa10"
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 404, "Not validating post request properly(sent wrong protocol), should returned 400, instead: %s" % r.status_code)

        data = {
            "caption": "Persiana terraza",
            "did": "A1",
            "protocol": "X10",
            "device_type": "claxon",
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 400, "Not validating post request properly(sent wrong device_type), should returned 400, instead: %s" % r.status_code)

        data = {
            "caption": "Persiana terraza",
            "protocol": "X10",
            "device_type": "dimmer",
            "did": "sa55",
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 400, "Not validating post request properly(sent wrong did), should returned 400, instead: %s" % r.status_code)

        data = {
            "did": "z5",
            "caption": "Persiana terraza",
            "protocol": "X10",
            "device_type": "dimmer",
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 400, "Not validating post request properly(sent wrong did), should returned 400, instead: %s" % r.status_code)

        data = {
            "did": "5a",
            "caption": "Persiana terraza",
            "protocol": "X10",
            "device_type": "dimmer",
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 400, "Not validating post request properly(sent wrong did), should returned 400, instead: %s" % r.status_code)

        data = {
            "did": "zz",
            "caption": "Persiana terraza",
            "protocol": "X10",
            "device_type": "dimmer",
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 400, "Not validating post request properly(sent wrong did), should returned 400, instead: %s" % r.status_code)

        data = {
            "caption": "Persiana terraza",
            "did": "A1",
            "device_type": "dimmer",
            "protocol": "X10"
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 200, "Not creating properly devices, returned: %s" % r.status_code)

        data = {
            "caption": "Persiana terraza",
            "did": "A1",
            "device_type": "dimmer",
            "protocol": "X10"
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)
        self.assertTrue(r.status_code == 409, "Not creating properly devices, returned: %s(should return 409(conflict))" % r.status_code)

        del_device("A1", self.live_server_url)

    def test_delete(self):
        print "running DeviceTest.delete ........................................"
        r = new_device("X10", "A3", "switch", self.live_server_url)

        print "errrr r:%s" % r.json()
        id = r.json()["did"]

        r = requests.delete("%s%s" % (self.live_server_url, reverse("device_by_id", args=[id])))
        self.assertTrue(r.status_code == 204, "No deleting property device, status returned: %s(should return 204)" % r.status_code)

        r = requests.delete("%s%s" % (self.live_server_url, reverse("device_by_id", args=[id])))
        self.assertTrue(r.status_code == 404, "No deleting property device, status returned: %s " % r.status_code)

    def test_get(self):
        print "Running DeviceTest.get.................................................."
        data = {
            "caption": "Persiana terraza",
            "did": "A2",
            "device_type": "dimmer",
            "protocol": "X10"
        }
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)

        data["did"] = "A21"
        data["caption"] = "persiana salon"
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)

        data["did"] = "A3"
        data["caption"] = "persiana cuarto"
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)

        data["did"] = "A4"
        data["caption"] = "persiana pasillo"
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)

        r = requests.get("%s%s?device_type=dimmer" % (self.live_server_url, reverse("device")))
        print r.json()
        self.assertTrue(len(r.json()) == 4, "Not creating devices properly or not retrieving")

        r = requests.get("%s%s?device_type=switch" % (self.live_server_url, reverse("device")))

        self.assertTrue(len(r.json()) == 0, "Not retrieving devices properly, asked for switch devices(only dimmer at db), should return 0, returned: %s" % len(r.json()))

        data["did"] = "A5"
        data["caption"] = "luz pasillo"
        data["device_type"] = "switch"
        r = requests.post("%s%s" % (self.live_server_url, reverse("device")), data=data)

        r = requests.get("%s%s?device_type=switch" % (self.live_server_url, reverse("device")))

        self.assertTrue(len(r.json()) == 1, "Not retrieving switches properly, should return 1, returned: %s" % len(r.json()))

        del_device("A2", self.live_server_url)
        del_device("A21", self.live_server_url)
        del_device("A3", self.live_server_url)
        del_device("A4", self.live_server_url)


class CmdTest(RestTest):
    def test_pl_switch(self):
        print "Running CmdTests.pl_switch ..............................................."
        r = new_device("X10", "A1", "switch", self.live_server_url)


        url = {
            "host": self.live_server_url,
            "path": reverse("pl_switch", kwargs={
                    "protocol": "X10",
                    "did": "A1",
                }),

        }
        data = {"value": "ON"}
        #r = requests.put("{host}{path}".format(**url), data=data)
        r = requests.request("PUT", "{host}{path}".format(**url), data=data)

        self.assertTrue(r.status_code == 200, "Not properly validating pl_switch values, sent uppercaer ON and didn't accept it\n%s" % show_response(r))

        data = {"value": "on"}
        r = requests.request("PUT", "{host}{path}".format(**url), data=data)
        self.assertTrue(r.status_code == 200, "Not properly validating pl_switch values, sent on and didn't accept it\n%s" % show_response(r))

        data = {"value": "OFF"}
        r = requests.request("PUT", "{host}{path}".format(**url), data=data)
        self.assertTrue(r.status_code == 200, "Not properly validating pl_switch values, sent uppercaer OFF and didn't accept it\n%s" % show_response(r))

        data = {"value": "off"}
        r = requests.request("PUT", "{host}{path}".format(**url), data=data)
        self.assertTrue(r.status_code == 200, "Not properly validating pl_switch values, sent on and didn't accept it\n%s" % show_response(r))

        data = {"value": "Odgdfg"}
        r = requests.request("PUT", "{host}{path}".format(**url), data=data)
        self.assertTrue(r.status_code == 400, "Not properly validating pl_switch values, sent invalid value and it accepted it\n%s" % show_response(r))


        url = {
            "host": self.live_server_url,
            "path": reverse("pl_switch", kwargs={
                    "protocol": "X10",
                    "did": "A1hh",
                }),

        }
        data = {"value": "Odgdfg"}
        r = requests.request("PUT", "{host}{path}".format(**url), data=data)
        self.assertTrue(r.status_code == 400, "Not properly validating X10 address, sent invalid did and it accepted it\n%s" % show_response(r))


        del_device("A1", self.live_server_url)
