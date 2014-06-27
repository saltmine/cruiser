from bs4 import BeautifulSoup
import requests

from ..models import images

img_replace = [('t_post_grid_progressive', 'f_png,fl_png8,c_pad,h_500,w_300')]


def crawl_page(url_template, page_number=None):
  url = url_template
  if page_number is not None:
    url = url_template % page_number
  print "crawling %s" % url

  soup = BeautifulSoup(requests.get(url).content)
  for i in soup.find_all("img", class_="i"):
    img_url = i.get('src')
    prod_id = i.get('data-id')
    text = i.get('alt', '')
    if img_url and prod_id:
      for r in img_replace:
        img_url = img_url.replace(r[0], r[1])
      keep_url  = "http://keep.com/slug/k/%s" % prod_id
      images.create_to_classify(prod_id, img_url, keep_url, text)
