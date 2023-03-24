import pika

_credentials=pika.credentials.PlainCredentials('ictu', 'ictu')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(credentials=_credentials)
)
