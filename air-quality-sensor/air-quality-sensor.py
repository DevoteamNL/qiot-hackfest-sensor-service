import tornado.ioloop
import tornado.web
import datetime
from enviroplus import gas

class GasHandler(tornado.web.RequestHandler):
    def get(self):
        gas_reading = {}
        # gas.enable_adc(True)
        readings = gas.read_all()

        gas_reading["instant"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        gas_reading["adc"] = readings.adc
        gas_reading["nh3"] = readings.nh3
        gas_reading["oxidising"] = readings.oxidising
        gas_reading["reducing"] = readings.reducing

        self.write(gas_reading)

def make_app():
    return tornado.web.Application([
        (r"/gas", GasHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()