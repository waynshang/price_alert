import requests
from utils import get_keys, get_values, create_dict_from_variables
import json
DETAIL_ALLOW_COLUMN={
  "originPrice": "originPrice",
  "minPrice": "minPrice",
}
HEADER = {"User-Agent":"Mozilla/5.0", 
'Accept': '*/*', 
'Cookie': '__cfduid=d14358f14b8ab9565814ae868b48b3e951612274817', 
'Connection': 'keep-alive',
'Content-Type': 'application/json'}

class UniqloController:
  def __init__(self, param):
    self.country_code=  param['country_code'] if 'country_code' in param else 'tw'
    self.language_code= param['language_code'] if 'language_code' in param else 'zh_TW'
    self.product_code= param['product_code']
  
  def get_product_detail(self):
    url = 'https://d.uniqlo.com/%s/p/product/i/product/spu/pc/query/%s/%s' % (self.country_code, self.product_code, self.language_code)
    response = requests.get(url, headers=HEADER)
    return self.parse_product_detail_api_response(response)

  def parse_product_detail_api_response(self, response):
    result = {}
    response = self._prase_basic_uniqlo_api_response(response)
    if not response: return {}
    response = response[0]['summary']
    for key, value in response.items():
      if key in get_keys(DETAIL_ALLOW_COLUMN):
        result[DETAIL_ALLOW_COLUMN[key]] = value
    return result
  
  def get_promotion(self):
    url = 'https://d.uniqlo.com/%s/p/hmall-promotion-service/h/sale/calculation/optionByProductCode/%s' % (self.country_code, self.language_code)
    params = {'productCode': self.product_code}
    response = requests.get(url, params=params,headers=HEADER)
    return self._prase_basic_uniqlo_api_response(response)

  def check_has_stock(self):
    url = 'https://d.uniqlo.com/%s/p/stock/stock/query/%s' % (self.country_code, self.language_code)
    data = {
      "distribution": "EXPRESS",
      'productCode': self.product_code,
      "type": "DETAIL",
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    response = self._prase_basic_uniqlo_api_response(response)
    if not response: return False
    if response[0]['hasStock'] == 'Y':
      return True
    return False


  def _prase_basic_uniqlo_api_response(self, response):
    if not response: 
      return {}
    response = response.json()
    response = response['resp']
    if not response: 
      return {}
    return response


