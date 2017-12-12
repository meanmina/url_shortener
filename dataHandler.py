from databaseHandler import DatabaseHandler
from decoder import Decoder
from encoder import Encoder

import re

class DataHandler:
  databaseHandler = None
  decoder = None
  encoder = None

  def __init__(self):
    # create databaseHandler, decoder and encoder
    self.databaseHandler = DatabaseHandler()
    self.decoder = Decoder()
    self.encoder = Encoder()
    # check database is setup
    self.databaseHandler.checkDbs()

  def shortenUrl(self, url):
    # url validation
    regex = re.compile(
      r'^(?:http|ftp)s?://' # http:// or https://
      r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domains
      r'localhost|' # localhost
      r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ipv4
      r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ipv6
      r'(?::\d+)?' # optional port
      r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(url) is None:
      return None

    # add URL to database and get ID
    url_id = self.databaseHandler.addToDbs(url)

    if url_id:
      # return encoded version
      return self.encoder.encode(url_id)

    return None

  def getUrl(self, short_url):
    if len(short_url) == 0:
      return None
    # decode URL
    decoded_url = self.decoder.decode(short_url)
    # get original URL from database
    return self.databaseHandler.getFromDbs(decoded_url)
