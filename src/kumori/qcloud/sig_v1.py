import base64
import hashlib
import hmac
from typing import Iterable, Dict, Tuple


def expand(args, key=None):
    if isinstance(args, dict):
        for k, v in args.items():
            yield from expand(v, key+"."+k if key else k)
    elif isinstance(args, (list, tuple)):
        for i, v in enumerate(args):
            yield from expand(v, f'{key}.{i}' if key else str(i))
    else:
        assert key is not None, "key should not be None"
        yield key, args

def compose(kwargs: Dict, action: str, timestamp, nonce, region, version, sid):
    kwargs['Action'] = action
    kwargs['Nonce'] = nonce
    kwargs['Timestamp'] = timestamp
    kwargs['Nonce'] = nonce
    kwargs['Region'] = region
    kwargs['Version'] = version
    kwargs['SecretId'] = sid
    
    return sorted(list(expand(kwargs)))

def sign(skey: bytes, method: str, domain: str, path: str, args: Iterable[Tuple]):
    s = method + domain + path + '?' + '&'.join(f'{k}={v}' for k,v in args)
    hmac_str = hmac.new(skey, s.encode("utf8"), hashlib.sha1).digest()

    return base64.b64encode(hmac_str)
    