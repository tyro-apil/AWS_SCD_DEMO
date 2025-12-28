# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
import json
import random
import time

from awscrt import mqtt5
from awsiot import mqtt5_client_builder

# ------------------- ARGUMENTS -------------------
parser = argparse.ArgumentParser(description="Minimal MQTT5 X509 JSON Publisher")
parser.add_argument("--endpoint", required=True, help="IoT endpoint hostname")
parser.add_argument("--cert", required=True, help="Path to certificate file")
parser.add_argument("--key", required=True, help="Path to private key file")
parser.add_argument("--farm_id", required=True, help="Device Id")
parser.add_argument("--crop_name", required=True, help="Crop Name")
parser.add_argument(
    "--humid_low", type=float, default=1.0, help="Min value for humidity"
)
parser.add_argument(
    "--humid_high", type=float, default=1.0, help="Max value for humidity"
)
parser.add_argument(
    "--temp_low", type=float, default=1.0, help="Min value for temperature"
)
parser.add_argument(
    "--temp_high", type=float, default=1.0, help="Max value for temperature"
)
args = parser.parse_args()

INTERVAL = 60
TIMEOUT = 10
MAX_COUNT = 5000

# ------------------- MQTT CLIENT -------------------
client_id = f"{args.farm_id}_{args.crop_name}"
client = mqtt5_client_builder.mtls_from_path(
    endpoint=args.endpoint,
    cert_filepath=args.cert,
    pri_key_filepath=args.key,
    client_id=client_id,
)
topic = f"farms/{args.farm_id}/{args.crop_name}/data"

client.start()
time.sleep(1)  # Give time for connection

# ------------------- PUBLISH LOOP -------------------
count = 1
try:
    while count <= MAX_COUNT:
        humidity = random.uniform(args.humid_low, args.humid_high)
        temperature = random.uniform(args.temp_low, args.temp_high)
        payload = json.dumps({"humidity": humidity, "temperature": temperature})
        publish_future = client.publish(
            mqtt5.PublishPacket(
                topic=topic, payload=payload, qos=mqtt5.QoS.AT_LEAST_ONCE
            )
        )
        publish_future.result(TIMEOUT)
        print(f"[{count}] Published JSON to '{topic}': {payload}")
        count += 1
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nStopping publisher...")

finally:
    client.stop()
    print("Client stopped.")
