#!/usr/bin/env python
# -*- coding: ascii -*-

# run this script to listen all the messages with the same format used for exchanging 
# messages between the wrapper and the CHIC platform

__author__ = 'Simone Bna (simone.bna@cineca.it)'
__copyright__ = ''
__license__ = ''
__vcs_id__ = ''
__version__ = ''

import os
import json
import pika
from pika.exceptions import *

EXCHANGE_NAME = 'vphhf'

host = os.environ["AMQP_HOST"]
vhost = os.environ["AMQP_VHOST"]
port = int(os.environ["AMQP_PORT"])
user = os.environ["AMQP_USER"]
password = os.environ["AMQP_PASSWORD"]

credentials = pika.PlainCredentials(user, password)
parameters = pika.ConnectionParameters(host, port, vhost, credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_key = 'workflow.*.*.snapshot'

channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name,  routing_key=binding_key)

print(' [*] Waiting for notifications from ' + EXCHANGE_NAME + '. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r:%r" % (method.routing_key, body))
    print str(body)
    out = json.loads(str(body))
    print out

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
