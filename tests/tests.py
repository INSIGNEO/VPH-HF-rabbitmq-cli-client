#!/usr/bin/env python
# -*- coding: ascii -*-

# run this script to check if the dispatch and receiving messages from the message broker using the
# VPH-HF rabbitmq cli client works as expected

__author__ = 'Simone Bna (simone.bna@cineca.it)'
__copyright__ = ''
__license__ = ''
__vcs_id__ = ''
__version__ = ''

import os
import json
import pika
from pika.exceptions import *
from subprocess import call
from threading import Thread
import time
import datetime
import json
import unittest


## Unittests for the VPH-HF rabbitmq cli client
class VPHHFRabbitmqCLIClientTest(unittest.TestCase):
  
    # Test the dispatch and receiving a message from the message broker using the 
    # VPH-HF rabbitmq cli client
    def test_send_receive(self):

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

        print(' [*] Waiting for notifications from ' + EXCHANGE_NAME)

        def callback(ch, method, properties, body):
            print(" [x] Received %r:%r" % (method.routing_key, body))
            json_str_body_to_be_checked = "{\"hypomodel_uuid\" : \"123e4567-e89b-12d3-a456-426651440000\", \
\"status\":\"FINISHED_SUCCESSFULLY\", \"output_values\": {\"223e4567-e89b-12d3-a456-426655440000\" : \
\"/home/vphhf/test\", \"123e4561-e89b-12d3-a456-426655440000\" : \"12567\"}}"
            if str(body) == json_str_body_to_be_checked:
                ch.test_error_message = 'ok'
            else:
                ch.test_error_message = 'error'
            ch.stop_consuming()

        channel.basic_consume(callback, queue=queue_name, no_ack=True)

        def listen_test_message(channel):
            channel.start_consuming()
    
        def send_test_message():
            call(["bash", "wrapper_test_dispatcher.sh"])

        t1 = Thread(target=listen_test_message, args=(channel,))
        t2 = Thread(target=send_test_message)

        t1.start()
        time.sleep(2)
        t2.start()

        t1.join(20)
        t2.join(20)

        self.assertEqual(channel.test_error_message, 'ok')


print "This is a test on the VPH-HF rabbitmq cli client"
print "The test starts at " + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
print ""

suite = unittest.TestLoader().loadTestsFromTestCase(VPHHFRabbitmqCLIClientTest)
unittest.TextTestRunner(verbosity=2).run(suite)