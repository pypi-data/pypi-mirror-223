from functools import wraps
import binascii,time,os
from flask import request,jsonify


def err(msg):
    return jsonify({'code':1,'msg':msg})


def insert_cover(db,info):
    max_id = list(db.find().sort('id',-1).limit(1))
    if len(max_id):
        id_ =  max_id[0]['id']+1
    else:
        id_ = 1
    info['id'] = id_
    info['created_time'] = int(time.time())
    info['update_time'] = int(time.time())
    return info



def safe_dict(dict_,key_list,skip_null=False):
    if not dict_:
        return []
    new_dict = {}
    for key in key_list:
        if skip_null:
            if dict_.get(key,None):
                new_dict[key] = dict_.get(key)
        else:
            new_dict[key] = dict_.get(key,None)
    return new_dict

def create_token(lenth=24):
    """创建一个token"""
    s = binascii.b2a_base64(os.urandom(lenth))[:-1].decode('utf-8')
    for x in ['+','=','/','?','&','%',"#"]:
        s = s.replace(x,"")
    return s

    

def json_require(info,method='POST'):
    def decorator(f):
        @wraps(f)
        def decorated_function():
            return_info = {}
            if method=="POST":
                dic = request.json 
            else:
                dic = request.args
            if not dic:
                return jsonify({'code':1,'msg':f"requir parameters"})
            keys = list(dic.keys())
            for name in info:
                content = dic.get(name)
                if not content:
                    return jsonify({'code':1,'msg':f"required {name}"})
                type_ = info[name]
                try:
                    if type_=="int":
                        return_info[name] = int(content)
                    elif type_=="string":
                        return_info[name]  = str(content)
                    elif type_=="list":
                        return_info[name]  = list(content)
                    elif type_=="bool":
                        return_info[name]  = bool(content)

                except Exception as e:
                    return jsonify({'code':1,'msg':f"The field {name} should be of type {type_}"})
            for x in keys:
                if x not in list(info.keys()):
                    return_info[x] = dic.get(x)             
            return f(return_info)
        return decorated_function
    return decorator

