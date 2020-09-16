import tornado.ioloop
import tornado.web
import time
from enviroplus import gas

class GasHandler(tornado.web.RequestHandler):
    def get(self):
        gas_reading = {}

        readings = gas.read_all()
        logging.info(readings)


        # gas_reading["instant"] = "timestamp"
        # gas_reading["adc"] = "blah"
        # gas_reading["nh3"] = "blah"
        # gas_reading["oxidising"] = "blah"
        # gas_reading["reducing"] = "blah"

        self.write(readings)

def make_app():
    return tornado.web.Application([
        (r"/gas", GasHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()