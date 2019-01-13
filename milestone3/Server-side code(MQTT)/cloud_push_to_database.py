import base64
from google.cloud import bigquery


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    data = pubsub_message.split(",")
    mode = "normal"
    hr = int(data[0])

    if data[1] == "1":
        mode = "pacemaker used freq"
    if data[2] == "1" and mode == 'normal':
        mode = "heart beating too fast"
    if data[2] == "1" and mode == "pace maker used freq":
        mode = "pace maker used freq AND heart beating too fast"

    print("HR:" + str(hr))
    print("Mode:" + mode)

    client = bigquery.Client()

    query3 = "INSERT INTO heart.raw_data_hr (deviceID, timestamp, avg_hr, mode) VALUES ('mbed', CURRENT_TIMESTAMP(), "+str(hr)+",'"+mode+"')"

    queryjob = client.query(query3,location="US",)

    for row in queryjob:
        print(row)


    
