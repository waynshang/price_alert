import requests
from utils import get_keys,get_object_by_keys
import json
DETAIL_ALLOW_COLUMN={
  "originPrice": "originPrice",
  "minPrice": "minPrice",
}
HEADER = {"User-Agent":"Mozilla/5.0", 
'Accept': '*/*', 
'Connection': 'keep-alive',
'Content-Type': 'application/json'}

class UniqloController:
  def __init__(self, param):
    self.country_code=  param['country_code'] if 'country_code' in param else 'tw'
    self.language_code= param['language_code'] if 'language_code' in param else 'zh_TW'
    self.product_code= param['product_code'] if 'product_code' in param else None
    self.item_code= str(param['item_code']).ljust(9, '0') if 'item_code' in param else None

  def get_product_detail(self):
    if not self.product_code: return {}
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
    if not self.product_code: return {}
    url = 'https://d.uniqlo.com/%s/p/hmall-promotion-service/h/sale/calculation/optionByProductCode/%s' % (self.country_code, self.language_code)
    params = {'productCode': self.product_code}
    response = requests.get(url, params=params,headers=HEADER)
    return self._prase_basic_uniqlo_api_response(response)

  def check_has_stock(self):
    if not self.product_code: return False
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
  
  def get_picture_urls(self):
    if not self.item_code: return []
    url = 'https://style.uniqlo.com/api/v2/searchItemCode.json?limit=-1&locale=%s&item_code=%s' % (self.country_code, self.item_code)
    response = requests.get(url, headers=HEADER)
    return self.parse_search_item_code_api_response(response)
  
  def parse_search_item_code_api_response(self, response):
    if not response: 
      return []
    response = response.json()
    item_data = get_object_by_keys(response, ['result', 'styles', self.item_code])
    if not item_data: 
      return []
    style_image_urls = []
    for style_data in item_data:
      style_image_urls.append('https:' + style_data['styleImgUrl'])
    return style_image_urls


  def _prase_basic_uniqlo_api_response(self, response):
    if not response: 
      return {}
    response = response.json()
    if 'resp' not in response: 
      return {}
    response = response['resp']
    if not response: 
      return {}
    return response


