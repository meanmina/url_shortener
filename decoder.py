import string
from math import floor

class Decoder:
  # use this to decode Base62 string to URL
  def decode(self, inpt, base=62):
    # base validation
    if base <= 0 or base > 62:
          return 0

    # we want combinations of [a-z][A-Z][0-9]
    the_base = string.digits + string.lowercase + string.uppercase

    result = 0
    # loop through every element in inpt
    for i in range(len(inpt)):
      # add new decoded to the result
      result = base * result + the_base.find(inpt[i])
    return result