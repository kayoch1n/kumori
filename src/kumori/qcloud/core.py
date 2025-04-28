from dataclasses import dataclass
from typing import Dict
import functools
import time

from kumori.qcloud import sig_v1


class Console:
    def __init__(self, domain='tencentcloudapi.com'):
        self.domain = domain
        self.services = {}
        
    def add_service(self, name, version):
        s = self.services[name] = Service(name, version, self.domain, {})
        return s
        
    def get_service(self, name):
        return self.services[name]

@dataclass
class Service:
    name: str
    version: str
    domain: str
    
    actions: Dict[str, str]

    

console = Console()
console.add_service('cvm', '2017-03-12')


class User:
    def __init__(self, sid: str, skey: str, region: str, console=console):
        self.console = console
        self.sid = sid
        self.skey = skey
        self.region = region
        
    def __getattr__(self, name):
        return UserContext(self, self.console.get_service(name))


@dataclass    
class UserContext:
    user: User
    service: Service
    
    @functools.cache
    def get_action(self, name):
        def func(**kwargs):
            
            sig_v1.compose(
                kwargs, 
                name, 
                int(time.time()), 
                114514, 
                self.user.region,
                self.service.version,
                self.user.sid)
        
        return func
    
    def __getattr__(self, name):
        return self.get_action(name)