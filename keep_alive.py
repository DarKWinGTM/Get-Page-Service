import uuid
import logging
from flask import Flask
from threading import Thread
import _thread

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask('')

@app.route('/', methods = ['POST', 'GET'])
def index():
    return "I'm alive"

def run():
    app.config['SECRET_KEY']                = uuid.uuid4().hex
    app.run( host = '0.0.0.0', port = 5000, threaded = True )
    # app.run(host='0.0.0.0', port=8080)

def keep_alive():
    #   t = Thread(target=run)
    #   t.start()
    from gevent import monkey
    monkey.patch_all()
    _thread.start_new_thread(run, ())
