import hashlib
import time
import re
import os
import random
import json
import math


class funcs():
    def md5(self, str):
        return hashlib.md5(str.encode('utf-8')).hexdigest()

    def coalesce(self, val, ret_val=None):
        if val is None:
            return ret_val
        else:
            return val

    def decode_user_confirm_hash(self, _hash):
        trans_user_id = int(_hash[7:][:-20])
        return int((trans_user_id + 777) / 13)

    def is_valid_password_format(self, s):
        if (len(s) < 8):
            return False
        if (re.search("^[\d]+$", s)):
            return False
        if (re.search("^([^\d]*)$", s)):
            return False
        return True

    def is_valid_nick_format(self, s):
        if( re.search("^[\wა-ჰа-я\d\-\_\.\'\;]{2,30}$", s) ):
            return True
        return False

    def get_json(self, v):
        try:
            if(v == None):
                raise ValueError
            ret_json = json.loads(v)
            return ret_json
        except ValueError as e:
            return False

    def is_valid_md5(self, str):
        return re.search('^[0-9a-fA-F]{32}$', str)

    def ctype_digit(self, v):
        try:
            if (v == None):
                raise ValueError
            int(str(v)) # cast to str needed becuase if float value is passed, then casting to int does not riases exception
            return True
        except ValueError:
            return False

    def disposable_session_set(self, req, key, val):
        req.session['disposable_sess_'+key] = val

    def disposable_session_get(self, req, key):
        key = 'disposable_sess_' + key
        if(req.session.get(key) == None):
            #print("noneeeeeeeeeeeeeeeeeeeee:::")
            return None
        else:
            ret = req.session.get(key)
            req.session[key] = None
            del req.session[key]
            # print("rrrrrrrrrrr111:")
            # print(ret)
            return ret



    ### upload image handler START
    def check_mime_type(self, file, allowed_mime_types):
        mime_type = mimetypes.guess_type(file)[0]
        print(mime_type)
        if mime_type in allowed_mime_types:
            return True

        return False

