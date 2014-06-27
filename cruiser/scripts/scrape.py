from ..controllers.scraper import crawl_page

def crawl_trending(num_pages):
  crawl_url('http://keep.com/%d/', num_pages)

def crawl_url(url_template, num_pages):
  for i in range(int(num_pages)):
    crawl_page(url_template, i)
