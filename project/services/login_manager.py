from hashlib import sha512
import time, random, json, hmac, base64
from django.core.cache import caches
from project.settings import SECRET_KEY, USER_TOKEN_TIMEVALID
from uuid import uuid4

token_cache = caches["tokens"]

def login_user(user:object, timevalid:float=USER_TOKEN_TIMEVALID):
    token_id = str(uuid4())
    token_cache.set(token_id, user.id, timevalid)
    token_data = {"token":token_id, "user":user.id}
    public_str = base64.b64encode(json.dumps(token_data).encode()).decode()
    signed_str = hmac.new(SECRET_KEY.encode(), public_str.encode(), sha512).hexdigest()
    token = f"{public_str}.{signed_str}"
    return {"token":token,"timevalid":time.time()+timevalid, "token_id":token_id}


def logout_user(request):
    user = request.customer
    token = request.token
    token_cache.delete(token)
    login = user.logins.get(token=token)
    login.is_active = False
    login.save()
    return "success"


def login_leader(leader:object, timevalid:float=USER_TOKEN_TIMEVALID):
    token_id = str(uuid4())
    token_cache.set(token_id, leader.id, timevalid)
    token_data = {"token":token_id, "leader":leader.id}
    public_str = base64.b64encode(json.dumps(token_data).encode()).decode()
    signed_str = hmac.new(SECRET_KEY.encode(), public_str.encode(), sha512).hexdigest()
    token = f"{public_str}.{signed_str}"
    return {"token":token,"timevalid":time.time()+timevalid}


def logout_leader(request):
    leader = request.leader
    token = request.token
    token_cache.delete(token)
    return "success"