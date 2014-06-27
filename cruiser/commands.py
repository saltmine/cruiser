import newman

def main():
  """Entry point for command line access
  """
  cli = newman.Newman("Cruiser - product ranking tool", top_level_args={})

  import cruiser.scripts.web
  import cruiser.scripts.scrape

  cli.load_module(cruiser.scripts.web, 'web')
  cli.load_module(cruiser.scripts.scrape, 'scrape')

  cli.go()
