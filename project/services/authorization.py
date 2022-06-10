from hashlib import sha512
import hmac, json, base64

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import caches

from user.models import Leader, User
from project.settings import SECRET_KEY

token_cache = caches["tokens"]

class CustomAuthorization(MiddlewareMixin):

    def process_request(self, request):
        token = request.headers.get("Authorization")
        if token:
            if len(token.split()) == 2 and token.split()[0] == "Bearer":
                token = token.split()[1].split('.')
                if len(token) == 2:
                    try:
                        token_json = json.loads(base64.b64decode(token[0]).decode())
                    except json.decoder.JSONDecodeError as e:
                        return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
                    if isinstance(token_json, dict):
                        if list(token_json) == ["token","user"]:
                            if hmac.new(SECRET_KEY.encode(), token[0].encode(), sha512).hexdigest() == token[1]:
                                in_cache_token = token_cache.get(token_json["token"])
                                if in_cache_token and token_json["user"] == in_cache_token:
                                    request.token = token_json["token"]
                                    request.customer = User.objects.get(id=in_cache_token)
                                else:
                                    return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
                        elif list(token_json) == ["token","leader"]:
                            if hmac.new(SECRET_KEY.encode(), token[0].encode(), sha512).hexdigest() == token[1]:
                                in_cache_token = token_cache.get(token_json["token"])
                                if in_cache_token and token_json["leader"] == in_cache_token:
                                    request.token = token_json["token"]
                                    request.leader = Leader.objects.get(id=in_cache_token)
                                else:
                                    return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
                        else:
                            return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
                    else:
                        return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
                else:
                    return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
            else:
                return HttpResponse(content=json.dumps({"code":"unauthtenticated"}),status=401,content_type="application/json")
        else:
            pass
