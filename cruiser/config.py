import os

import redis

initialized = False

db_conn = None

def init():
  global db_conn
  global initalized
  if initialized:
    return
  db_conn = redis.StrictRedis(host='localhost', port=6379, db=22)

init()
