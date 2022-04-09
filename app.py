import os
from communicationApp import createClient
from controller import UniqloController
import json 

config_name = os.getenv('FLASK_CONFIG') or 'development'


def main():
  communication_app_name= 'telegram'
  bot_token = '1632387033:AAEgUxJiAwZBRVXwVpocXohQOxZYFhkkR6g'
  telegram = createClient(communication_app_name, bot_token = bot_token)
  params = {'product_code': 'u0000000011255'}
  uniqlo = UniqloController(params)
  product_detail = json.dumps(uniqlo.get_product_detail(), indent=2)
  promotion = uniqlo.get_promotion()
  has_stock = uniqlo.check_has_stock()

  telegram.send_message(f'product_detail: {product_detail}')
  telegram.send_message(f'promotion: {promotion}')
  telegram.send_message(f'has_stock: {has_stock}')


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    exit()