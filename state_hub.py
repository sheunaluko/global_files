# Tue Apr 30 01:26:14 PDT 2019
import utils as  u 
import asyncio 
import json 
import aiochan as ac 
import requests 
import sys 

# get logger and register with utils 
log = u.register("state_hub")

# define vars 
ws = None 
http_thread = None 
port = 9003
http_port = 9005 
task_library = {} 
remote_port = 9004 

# remote interface to run state_hub tasks 
def run_task(id,arg=None) : 
    log.i("Requesting to run task with id: {}".format(id))
    msg = { 'id' : id , 
            'arg' : arg  } 
    payload = { 'opts' : json.dumps(msg) } 
    r = requests.get('http://localhost:{}/run_task'.format(remote_port), params=payload)
    log.i("Got result: {}".format(r.text))         
    return r.json() 
    
def register_task(id,transition,se, info=None) : 
    global task_library     
    log.i("Registering task id: {}".format(id)) 
    task_library[id] = { 'transition' : transition , 
                         'se'         : se } 
    msg = { 'id' : id , 
            'http_port' : http_port , 
            'transition' : transition , 
            'info' : info } 
    
    payload = { 'opts' : json.dumps(msg) } 
    
    r = requests.get('http://localhost:{}/register'.format(remote_port), params=payload)
    log.i("Got result: {}".format(r.text))     

#local interface for state_hub core to trigger registered python tasks
def _run_task(msg) : 
    # will run a specified task - LOOK UP IN THE TASK LIB by ID 
    id = msg['id'] 
    log.i("Running task: {}".format(id))
    tsk = task_library[id] 
    
    if not tsk : 
        log.d("Could not find task: " + id ) 
        return {'error' : True , 'data' : "task not found" } 
    else : 
        log.d("Found task.") 
        try : 
            result = tsk['se'](msg.get('arg'))
            log.d("Got result: {}".format(result)) 
            return {'error' : False,  'data' : result} 
        except :
            return {'error' : True , 'data' : str(sys.exc_info()[0]) } 


# define functions for connecting to websocket 
async def on_connect(ws) : 
    log.i("Connected to remote state-hub server") 
    
    
def query_state(q) : 
    opts = {'query' : q  , 
            'length' : 20 } 
    payload = { 'opts' : json.dumps(opts) } 
    r = requests.get('http://localhost:9004/fulfill_state', params=payload)
    log.i("Got result: {}".format(r.text)) 
    return r 
    
    
def on_msg(message) : 
    msg = u.json_or_string(message) 
    log.i("Received msg: " + json.dumps(msg))
    
# - will create a http server for responding to task requests 
# - query is a JSON object 
def get_handler(query) : 
    log.i("Received query: {}".format(json.dumps(query)))
    # need to check for a message from trigger_task fn of core.js 
    if (query['type'] == 'run_task') : 
        log.i("recv run_task") 
        return _run_task(query) 
    else : 
        log.i("unkown request") 
        return None 

# - connect to statehub server 
def init(host='localhost',port=port,on_init=None) : 
    global ws 
    global http_thread 
    http_thread = u.http_server(9005,get_handler) 
    log.i("Initializing...") 
    if on_init : 
        on_init() 

    
    
test_query = { 'p' : [ 'tested-2' ] }     
def test_core() : 
    return query_state(test_query)

    










