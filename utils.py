import pprint
import builtins 
import glob 
import json 
import re 
import importlib 
import sys 
import math
import datetime 
import time 
import numpy as np 
import datetime 

#reloading stuff 
reload_children = set(["utils"] ) 
def register(f) : 
    reload_children.add(f) 
    mod = sys.modules[f] 
    def reloader() : 
        importlib.reload(mod) 
        print("Reloaded: " + f) 
    mod.r = reloader 
    
def r() : 
    global reload_children 
    children = reload_children 
    for m in reload_children : 
        print("reloading: " + m)
        mod = sys.modules[m]
        importlib.reload(mod) 
    reload_children = children 

    
# params , referenc , etc .. 

    
#strings and files 
def stringify_list_sep(l,sep) : 
    if isinstance(l, list) : 
        return  sep.join(l) 
    else :
        return l
    
def stringify_list(l) : 
    return stringify_list_sep(l, ",")


def acopy(tmp) : 
    str = tmp.encode() 
    from subprocess import Popen, PIPE
    p = Popen(['xsel', '-bi'], stdin=PIPE)
    p.communicate(input=str)

def cwd() : 
    import os
    return os.getcwd() + "/" 

def ensure_slash(d) : 
    #make sure there is trailing slash 
    if not d[-1] == "/" : 
        d = d + "/" 
    return d 

def get_files_in_dir(d) : 
    fs = glob.glob(ensure_slash(d) + "*" ) 
    fs.sort()
    return fs
    
def write_json(fname, obj) : 
    with open(fname, 'w') as outfile : 
        json.dump(obj, outfile) 
    print("Wrote ", fname)

def read_json(fname) : 
    with open(fname) as f:
        data = json.load(f)
    return data 

def read_big_string(fname) : 
    result = "" 
    with open(fname) as f:
        while True:
            c = f.read(1024)
            if not c:
                break
            result += c 
    return result
            
def read_string(fname) : 
    with open(fname, 'r') as myfile:
        data=myfile.read()
    return data 

def lines(s) : 
    return s.split("\n")
    
def read_and_split_file(fname, splitter) : 
    s = read_big_string(fname) 
    lines = [ x for x in s.split(splitter) if x is not "" ] 
    return lines 

def read_split_map_file(fname,splitter,mapper) : 
    lines = read_and_split_file(fname, splitter) 
    return [ mapper(l) for l in lines if l ]  
        
def check_for_file(fname)  : 
    import os.path
    return os.path.isfile(fname) 


def append_file(fname, strang) : 
    if not check_for_file(fname) : 
        mode = 'w' 
    else : 
        mode = 'a+' 

    with open(fname, mode) as outfile : 
        outfile.write(strang)


def contains(a1,a2) :  
    return bool(re.search(a2, a1))


# functional 
def map(f,l ) : 
    return  [ f(x) for x in l ] 

def extract_field_from_list(l,f) : 
    return [ x[f] for x in l ] 

def find_duplicates(coll) :   
    #tags: count, unique , ext 
    seen = {}
    dupes = []
    for x in coll:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    return (seen,dupes) 

def group_info(coll) : 
    s,d = find_duplicates(coll) 
    total = sum(list(s.values()))
    for k,v in s.items() : 
        s[k] = {'frequency' : v , 
                'percentage' : v/total} 
    return s



# sub commands 
def sub_cmd(cmd,mode) : 
    import subprocess
    import sys
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    to_return = "" 
    if mode is "q" : 
        #do nothing 
        pass 
    else : 
        for c in iter(lambda: process.stdout.read(1), b''): 
            ch = c.decode()
            to_return += ch 
            if mode is "v" : 
                sys.stdout.write(ch)
    if mode is "s" : 
        return to_return 

def sub_cmd_v(cmd) : 
    return sub_cmd(cmd,"v")

def sub_cmd_q(cmd) : 
    return sub_cmd(cmd,"q")

def sub_cmd_s(cmd) : 
    return sub_cmd(cmd,"s")


    
#time stuff 
def ms_stamp_2_datetime(t) : 
    return datetime.datetime.fromtimestamp(t/1000) 

def t_stamp_2_datetime(t) : 
    return datetime.datetime.fromtimestamp(t) 


#data science 

def get_series(raw,k) : 
    return np.array(extract_field_from_list(raw, k)) 
        
def get_float_series(raw, k) : 
    return np.array(map(float, extract_field_from_list(raw, k)))

def get_date64_series(raw, k) : 
    return np.array(extract_field_from_list(raw, k), dtype=np.datetime64)


def _mean(coll) : 
    return sum(coll)/len(coll)

def _diff(coll) : 
    vs = [] 
    last_val = coll[0] 
    for i in coll[1:] : 
        vs.append(i-last_val) 
        last_val  = i 
    return vs 

def datetime_mean(dt_list) : 
    tstamps = [ x.timestamp() for x in dt_list ] 
    return datetime.datetime.fromtimestamp( _mean(tstamps) ) 

def datetime64_mean(dt_list) : 
    return np.datetime64(datetime_mean(map(lambda x: x.astype(datetime.datetime),dt_list))) 

def mean(coll) : 
    if type(coll[0]) == datetime.datetime : 
        return datetime_mean(coll) 
    elif type(coll[0]) == np.datetime64 : 
        return datetime64_mean(coll)
    else : 
        return _mean(coll) 
    

def apply_function_accross_collection_fields(coll,f) : 
    all_keys = coll[0].keys() 
    return_obj = {} 
    for k in all_keys : 
        return_obj[k] = f( extract_field_from_list(coll,k) ) 
    return return_obj 

def field_means(coll) : 
    return apply_function_accross_collection_fields(coll, mean) 
        
def test_data() : 
    res = [] 
    count = 0 
    for i in range(22) : 
        count += 1 
        tmp = { 'c' : count , 
                't' : datetime.datetime.now()  } 
        res.append(tmp) 
        time.sleep(0.5) 
        print(i)
    return res 
        
def partition(coll, group_size)  : 
    l = len(coll) 
    res  = [] 
    end = math.floor(l / group_size ) * group_size 
    for i in range(0, end+1 ,group_size) : 
        if i == end : 
            tmp = coll[end:] 
        else : 
            tmp = coll[i:i+group_size] 
        #add the sublist if it is not empty 
        if tmp != [] : 
            res.append(tmp)  
    return res 


def downsample_dict_list_mean(l, group_size) : 
    if not group_size : 
        return l 
    else : 
        return map(field_means , partition(l, group_size)) 

    
#memory and performance measures 
def now() : 
    return time.perf_counter() 

def time_function(f) : 
    t0 = now() 
    throw_away = f() 
    return now() - t0 

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    ##https://goshippo.com/blog/measure-real-size-any-python-object/ 
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, builtins.bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def sysbytes(d) : 
    return sys.getsizeof(d)  #returns size of data in bytes 
def ubytes(d) : 
    return get_size(d)  
def kbytes(d) :
    return ubytes(d)/1024  
def mbytes(d) : 
    return kbytes(d)/1024  
def gbytes(d) : 
    return mbytes(d)/1024
    
    


            

    
#printing 
pretty_printer = pprint.PrettyPrinter(indent=4)
def pretty(val) : 
    pretty_printer.pprint(val)
