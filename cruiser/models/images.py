import random

import elo

from .. import config

TO_CLASSIFY_KEY = 'cruiser:to_classify'
SAVED_KEY = 'cruiser:saved'
IGNORED_KEY = 'cruiser:ignored'
PRODUCT_INFO = 'cruiser:product_info:%s'

def save_product_info(product_id, image_url, link, text):
  """Save product info into our data store.  Doesn't do anything about
     what category it's in.
  """
  config.db_conn.hmset(PRODUCT_INFO % product_id,
      {'product_id': product_id,
       'image_url': image_url,
       'link': link,
       'text': text})


def get_product_info(product_id):
  """Retrieve information about a product by id.
  """
  return config.db_conn.hgetall(PRODUCT_INFO % product_id)


def create_to_classify(product_id, image_url, product_link, text):
  """if it's not ignored and the id is not in our system,
     create it in the to_classify set.
  """
  if get_score(product_id) is None:
    if not config.db_conn.sismember(IGNORED_KEY, product_id):
      save_product_info(product_id, image_url, product_link, text)
      config.db_conn.sadd(TO_CLASSIFY_KEY, product_id)


def get_to_classify():
  """pull a random product id from the to_classify group.
  """
  prod_id = config.db_conn.srandmember(TO_CLASSIFY_KEY)
  return get_product_info(prod_id)


def get_to_classify_count():
  """get the count of items to classify.
  """
  return config.db_conn.scard(TO_CLASSIFY_KEY)


def save_classify(product_id):
  """move a product from to_classify to saved.
  """
  config.db_conn.srem(TO_CLASSIFY_KEY, product_id)
  save_product(product_id)


def ignore_classify(product_id):
  """move a product from to_classify to ignored.
  """
  config.db_conn.srem(TO_CLASSIFY_KEY, product_id)
  config.db_conn.sadd(IGNORED_KEY, product_id)


def save_product(product_id):
  """if it's not already there or ignored, save the product to the saved set
     with a default score.
  """
  if get_score(product_id) is None:
    if not config.db_conn.sismember(IGNORED_KEY, product_id):
      config.db_conn.zadd(SAVED_KEY, 1000, product_id)


def image_count():
  """the overall count of images saved.
  """
  return config.db_conn.zcard(SAVED_KEY)


def set_score(product_id, score):
  config.db_conn.zadd(SAVED_KEY, score, product_id)


def get_score(product_id):
  return config.db_conn.zscore(SAVED_KEY, product_id)


def get_rank(product_id):
  return config.db_conn.zrank(SAVED_KEY, product_id)


def flush_bottom(min_score=100):
  to_ignore = config.db_conn.zrangebyscore(SAVED_KEY, '-inf', min_score)
  for p in to_ignore:
    set_ignored(p)


def set_ignored(product_id):
  config.db_conn.zrem(SAVED_KEY, product_id)
  config.db_conn.sadd(IGNORED_KEY, product_id)


def get_pair():
  rand_rank = random.randint(0, image_count()-1)
  first = get_product_info(
      config.db_conn.zrange(SAVED_KEY, rand_rank, rand_rank)[0])
  if not first:
    return (None, None)
  comp = get_product_info(get_competitor(first['product_id']))
  if random.randint(0, 1):
    return (first, comp)
  else:
    return (comp, first)


def get_competitor(product_id):
  my_rank = get_rank(product_id)
  total_images = image_count()
  # keep going until we find a target within bounds that's not this one.
  if total_images > 1:
    target_rank = -1
    while target_rank < 0 or target_rank >= total_images or \
        target_rank == my_rank:
      target_rank = int(random.gauss(my_rank, total_images/5.0))
    return config.db_conn.zrange(SAVED_KEY, target_rank, target_rank)[0]
  else:
    return None


def settle_victory(winner_id, loser_id):
  winner_score = get_score(winner_id)
  loser_score = get_score(loser_id)
  if None not in (winner_score, loser_score):
    new_scores = elo.rate_1vs1(winner_score, loser_score)
    set_score(winner_id, new_scores[0])
    set_score(loser_id, new_scores[1])


def get_range(start, stop, withscores=False):
  p_ids = config.db_conn.zrange(SAVED_KEY, start, stop, withscores=withscores)
  return [(get_product_info(p), s) for p, s in p_ids]


def get_rev_range(start, stop, withscores=False):
  p_ids = config.db_conn.zrevrange(SAVED_KEY, start, stop,
      withscores=withscores)
  return [(get_product_info(p), s) for p, s in p_ids]


def flush_db():
  config.db_conn.flushdb()


