from bills import bills
from amendments import amendments
import difflib as dl
def get_change(bill_number):
 s1 = bills[bill_number]
 s2 = amendments[bill_number]

  return {'changes':  amendments[bill_number]};{ bills[bill_number]}