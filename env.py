import os

from dotenv import load_dotenv

load_dotenv()

#Server env
LISTEN_PORT = os.getenv('LISTEN_PORT','1667')
LISTEN_ADRESS = os.getenv('LISTEN_ADRESS','0.0.0.0')

#Web env
CUSTOMER_PORTAL_NAME = os.getenv('CUSTOMER_PORTAL_NAME','Customer Portal')

print(LISTEN_PORT,LISTEN_ADRESS)