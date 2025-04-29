import base64
import hashlib
import hmac
from typing import Iterable, Dict, Tuple


def expand(args: Dict, dst: Dict, key=None):
    if isinstance(args, dict):
        for k, v in args.items():
            expand(v, dst, key + "." + k if key else k)
    elif isinstance(args, (list, tuple)):
        for i, v in enumerate(args):
            expand(v, dst, f"{key}.{i}" if key else str(i))
    else:
        assert key is not None, "key should not be None"
        dst[key] = args


def compose(kwargs: Dict, action: str, timestamp, nonce, region, version, sid):
    ret = {}
    ret["Action"] = action
    ret["Nonce"] = nonce
    ret["Timestamp"] = timestamp
    ret["Nonce"] = nonce
    ret["Region"] = region
    ret["Version"] = version
    ret["SecretId"] = sid
    expand(kwargs, ret)
    return ret


def sign(skey: bytes, method: str, domain: str, path: str, args: Dict):
    args = sorted([(k, v) for k, v in args.items()])
    s = method + domain + path + "?" + "&".join(f"{k}={v}" for k, v in args)
    hmac_str = hmac.new(skey, s.encode("utf8"), hashlib.sha1).digest()

    return base64.b64encode(hmac_str)
