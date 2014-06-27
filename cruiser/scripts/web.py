from cruiser.web import cruiser_site
from cruiser.models import images

def run_server():
  cruiser_site.app.run('0.0.0.0', port=5002, debug=True)

def flush():
  images.flush_db()

