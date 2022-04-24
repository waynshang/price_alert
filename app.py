import os
from communicationApp import createClient
from controller import UniqloController
import json 
import config

config_name = os.getenv('FLASK_CONFIG') or 'development'


def main():
  communication_app_name= 'telegram'
  bot_token = config.bot_token
  telegram = createClient(communication_app_name, bot_token = bot_token)
  # TODO 
  product_code = 'u0000000011255'
  item_code = 444591

  params = {'product_code': product_code, 'item_code': item_code}
  uniqlo = UniqloController(params)
  product_detail = json.dumps(uniqlo.get_product_detail(), indent=2)
  promotion = uniqlo.get_promotion()
  has_stock = uniqlo.check_has_stock()
  picture_urls = uniqlo.get_picture_urls()

  telegram.send_message(f'product_detail: {product_detail}')
  telegram.send_message(f'promotion: {promotion}')
  telegram.send_message(f'has stock: {has_stock}')
  for picture_url in picture_urls:
    telegram.send_photo(image_url=str(picture_url))


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    exit()