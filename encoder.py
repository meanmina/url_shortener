import string
from math import floor

class Encoder:
  # use this to encode URL to Base62 string
  def encode(self, inpt, base=62):
    # base validation
    if base <= 0 or base > 62:
      return 0

    # we want combinations of [a-z][A-Z][0-9]
    the_base = string.digits + string.lowercase + string.uppercase

    remainder = inpt % base
    result = the_base[remainder]

    quotient = floor(inpt / base)
    # loop and keep dividing
    while quotient:
      remainder = quotient % base
      quotient = floor(quotient / base)
      # add new encoded to the result
      result = the_base[int(remainder)] + result
    return result