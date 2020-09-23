import tornado.ioloop
import tornado.web
import datetime
from enviroplus import gas
from pms5003 import PMS5003, ReadTimeoutError
import logging
import time

class GasHandler(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        gas_reading = {}
        gas.enable_adc()
        gas.set_adc_gain(4.096)
        readings = gas.read_all()

        gas_reading["instant"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        gas_reading["adc"] = readings.adc
        gas_reading["nh3"] = readings.nh3
        gas_reading["oxidising"] = readings.oxidising
        gas_reading["reducing"] = readings.reducing

        self.write(gas_reading)


class PollutionHandler(tornado.web.RequestHandler):
    def initialize(self, pms5003):
        self.pms5003 = pms5003
    
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        pollution_reading = {}
        readings = self.pms5003.read()

        pollution_reading["instant"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        pollution_reading["pm1_0"] = readings.pm_ug_per_m3(1.0)
        pollution_reading["pm2_5"] = readings.pm_ug_per_m3(2.5)
        pollution_reading["pm10"] = readings.pm_ug_per_m3(10)

        pollution_reading["pm1_0_atm"] = readings.pm_ug_per_m3(1.0,True)
        pollution_reading["pm2_5_atm"] = readings.pm_ug_per_m3(2.5,True)
        pollution_reading["pm10_atm"] = readings.pm_ug_per_m3(None,True)

        pollution_reading["gt0_3um"] = readings.pm_per_1l_air(0.3)
        pollution_reading["gt0_5um"] = readings.pm_per_1l_air(0.5)
        pollution_reading["gt1_0um"] = readings.pm_per_1l_air(1.0)
        pollution_reading["gt2_5um"] = readings.pm_per_1l_air(2.5)
        pollution_reading["gt5_0um"] = readings.pm_per_1l_air(5)
        pollution_reading["gt10um"] = readings.pm_per_1l_air(10)
        self.write(pollution_reading)


class HealthHandler(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        health_status = {}
        health_status["status"] = "UP"
        health_status["checks"] = "[]"
        self.write(health_status)


def make_app():
    # Initialize particulate sensor at application start
    pms5003 = PMS5003(
                   device='/dev/ttyAMA0',
                   baudrate=9600,
                   pin_enable=22,
                   pin_reset=27
                )
    return tornado.web.Application([
        (r"/gas", GasHandler),
        (r"/pollution", PollutionHandler, dict(pms5003=pms5003)),
        (r"/health", HealthHandler)
    ])

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    app = make_app()
    logging.info("Sensor service is starting...waiting 30 seconds to initialize..")
    time.sleep(30.0)
    logging.info("Initialization complete, started API server.")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()