import os
import sys
import json
import tornado.web
import tornado.escape
# import logic.dtm as dtm

# print sys.modules
if 'logic.dtm' not in sys.modules:
    import logic.dtm as dtm
else:
    dtm = sys.modules['logic.dtm']

timeout = 5 #cuanto se espera
#ctes que responden los tipos de solicitudes. 
REQUEST = 'REQUEST'
REQUEST_ANSWER = 'REQUEST_ANSWER'
EXCHANGE = 'vuelos.registrar.test'
ROUTING_KEY = 'vuelos.registrar.app2'
GENERAL_KEY = 'vuelos.registrar'
APP = 'app2'

results = {}

@tornado.gen.coroutine
def on_message(mq, _id, _from, status, to, message):
    # print 'to' + to
    # print 'message' + message
    # print 'from' + _from
    # print 'id' + _id
    # print 'status' + status
    if _from != APP:
        if status == REQUEST:
            print REQUEST
            local_videos = yield dtm.dar_usuarios_local()
            print local_videos
            mq.send_message(local_videos, EXCHANGE, ROUTING_KEY, to, REQUEST_ANSWER, _id)
        elif status == REQUEST_ANSWER:
            if _id in results:
                print message
                results[_id].append(message)

@tornado.gen.coroutine
def dar_usuarios_registrar(mq):
    _id = mq.send_message('', EXCHANGE, ROUTING_KEY, GENERAL_KEY, REQUEST)
    results[_id] = []
    yield tornado.gen.sleep(timeout)
    response = results.pop(_id)
    response = [x['usuarios'] for x in response]
    response = reduce(lambda x, y: x+y, response, [])
    print response
    raise tornado.gen.Return(response)