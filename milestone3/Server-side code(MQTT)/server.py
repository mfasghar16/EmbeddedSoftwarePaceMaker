# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, request, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from google.cloud import bigquery


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '35.196.225.7'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'mbed'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = 'homework'  # set the password here if the broker demands authentication
app.config['MQTT_CLIENT_ID'] = '26013f37-10000015100000161000001710000018'
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['SECRET_KEY'] = 'cis441finalproject'
socketio = SocketIO(app)
mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	print("MQTT Connect!")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	data = dict(topic=message.topic,payload=message.payload.decode())
	emit('hrData', {'data': data})
	print(data)

def callback(message):
    print('Received message: {}'.format(message))
    message.ack()

def query_hr():
    client = bigquery.Client()
    query = "SELECT timestamp, avg_hr, mode FROM heart.raw_data_hr ORDER BY timestamp"
    query_job = client.query(query)

    return query_job.result()


@app.route('/')
def hello():
	mqtt.subscribe('cis541/hw-mqtt/26013f37-10000015100000161000001710000018/echo')
	results = query_hr()
	return render_template("heart.html", results=results)


if __name__ == '__main__':
	socketio.run(app)
