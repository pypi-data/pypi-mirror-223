"""junoplatform.io.utils.py: implements helper tools"""
__author__      = "Bruce.Lu"
__email__       = "lzbgt@icloud.com"
__time__ = "2023/07/20"


from elasticsearch import Elasticsearch
import clickhouse_connect
import pymongo
from questdb.ingress import Sender, IngressError, TimestampNanos, TimestampMicros
import oss2
from itertools import islice
import pulsar
import re
import sys
import traceback
import time
import uuid
import logging
from urllib.parse import urlparse
from clickhouse_connect.driver import Client as CHClient
import yaml
import redis
from datetime import timedelta
import uuid
import json

def get_package_path(cfg: dict, package_id: str):
    plant = cfg['plant']
    module = cfg['module']
    
    return f"dist/{plant}-{module}-{package_id}.zip"
def api_url_():
    api_url = "http://192.168.101.157:8823/api"
    if "api_url" in driver_cfg:
        api_url = driver_cfg["api_url"]
    return api_url
    
          
driver_cfg:dict = {}
try:
    driver_cfg = yaml.safe_load(open('project.yml', 'r'))
except:
    pass

input_cfg: dict = {}
try:
    input_cfg = json.load(open('input.json', 'r'))
except:
    pass

module = driver_cfg.get('module')
plant = driver_cfg.get('plant')
package_id = driver_cfg.get('package_id')
version = driver_cfg.get('version')
api_url = api_url_()
instance_id = uuid.uuid4().hex

def redis_cli(host: str, port: int, password:str, db:int=0, socket_timeout = 3):
    logging.debug(f"local redis: {host}:{port} {db} {password}")
    return redis.Redis(host, port, db, password, socket_timeout=socket_timeout)
     
def pulsar_cli(url:str, shared: bool = False, ca:str="certs/ca.cert.pem",
               cert:str="certs/client.cert.pem", key:str="certs/client.key-pk8.pem"):
    client: pulsar.Client
    if 'ssl' in url:
        auth = pulsar.AuthenticationTLS(cert, key)
        client = pulsar.Client(url,
                        tls_trust_certs_file_path=ca,
                        tls_allow_insecure_connection=False,
                        authentication=auth)
    else:
        client = pulsar.Client(url)
        
    return client


def es_cli(url:str, ca:str, user:str, password:str):
    #cfg['elastic']['url'], ca_certs=cfg['elastic']['ca'], 
    #basic_auth=(cfg['elastic']['user'], cfg['elastic']['password'])
    return Elasticsearch(url, ca_certs=ca, basic_auth=(user, password))


def clickhouse_cli(url: str):
        p = urlparse(url)
        schema = p.scheme
        if schema != 'ch':
            raise Exception(f'invalid schema in dbs.clickhouse.url: {url}')
        user = p.username
        password = p.password
        host = p.hostname
        port = p.port
        return clickhouse_connect.get_client(host=host, username=user, 
                                            password=password, port=port)

# auth = ("pulsar", "KA6oqjb0s5OP49WHfKLabO8ef42ArV_9q9NznHNKUJ8", "_lTCuKKqtRWVDyb9d5545s99VwXVkJjs-HhCtPxPaTQ", "afh08JDKKYUxPYuHCWsytHQ7LgUZ63s-CTvTFaWFVE4")
def qdb_cli(host:str, port: str, auth: str, tls: bool, auto_flush: bool, **kwargs):
     auth_t = tuple(auth.split(' '))
     s = Sender(host, port, auth=auth_t, tls=tls, auto_flush=auto_flush)
     s.connect()
     return s
          

def mongo_cli(url: str):
    return pymongo.MongoClient(url)

def oss_cli(key:str, sec:str, endpoint:str, bucket: str):
    auth = oss2.Auth(key, sec)
    endpoint = endpoint
    r = oss2.Bucket(auth, endpoint, bucket, connect_timeout=5)
    # for b in islice(oss2.ObjectIterator(r), 10):
    #     print(b.key)
    return r
