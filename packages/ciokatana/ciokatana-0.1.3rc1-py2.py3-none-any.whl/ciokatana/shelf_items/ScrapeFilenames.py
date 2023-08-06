"""
NAME: ScrapeFilenames
ICON: icon.png
KEYBOARD_SHORTCUT: 
SCOPE:
Scrape Filenames


"""
from Katana import NodegraphAPI
import importlib
from ciokatana.v1 import reloader
from ciokatana.v1.model.asset_scraper import AssetScraper

importlib.reload(reloader)

reloader.reload()

import re


def is_absolute_filename(filename):
    # Regular expression patterns for different file systems
    posix_pattern = r'^/.*$'
    windows_pattern = r'^[a-zA-Z]:\\.*$'
    unc_pattern = r'^\\\\.*$'

    # Check if the filename matches any of the patterns
    if re.match(posix_pattern, filename) or \
       re.match(windows_pattern, filename) or \
       re.match(unc_pattern, filename):
        return True
    else:
        return False

print("Scraping filenames...")
scraper =  AssetScraper()
print("Instance created.")
scraper.scrape()
print("Scraping complete.")
filenames = scraper.dbg_filenames
# print("Filenames scraped.", len(filenames))
# filenames  = [ a for a in filenames if is_absolute_filename(a)]
# print("Absolute filenames filtered.", len(filenames))
# filenames = list(set(filenames))
# print("Unique filenames filtered.", len(filenames))

for f in scraper.dbg_filenames:
    # if is_absolute_filename(f):
    print(f)
    