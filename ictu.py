import pika
from dotenv import load_dotenv
from os import getenv

load_dotenv()

_credentials=pika.credentials.PlainCredentials(getenv('RABBITMQ_DEFAULT_USER'), getenv('RABBITMQ_DEFAULT_PASS'))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(credentials=_credentials)
)
