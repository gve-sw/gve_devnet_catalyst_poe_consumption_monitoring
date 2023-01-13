"""
Copyright (c) 2022 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import collector
import influxDB
import os
import time
from dotenv import load_dotenv

load_dotenv()

interval_minutes = int(os.getenv('COLLECTION_INTERVAL_MINUTES'))
testbed_filename = os.getenv('TESTBED_FILENAME')
command = "show power inline"

influxdb_host = os.getenv('INFLUX_HOST')
influxdb_port = os.getenv('INFLUX_PORT')
influxdb_username = os.getenv('INFLUX_USERNAME')
influxdb_password = os.getenv('INFLUX_PASSWORD')
influxdb_bucket = os.getenv('INFLUX_BUCKET')
influxdb_token = os.getenv('INFLUX_TOKEN')
influxdb_org = os.getenv('INFLUX_ORG')

kWh_price = float(os.getenv('kWh_PRICE'))

if __name__ == "__main__":

    collector = collector.Collector(testbed_filename, command)
    db = influxDB.InfluxDB(influxdb_host, influxdb_port, influxdb_token, influxdb_org, influxdb_bucket, kWh_price)
    
    while True:
        
        collector_data = collector.parse_all_devices()

        influx_data = db.convert_collector_to_influx_format(collector_data)
        db.syncronous_write(influx_data)

        print(f"Next sync in {interval_minutes} min")
        time.sleep(interval_minutes*60)


    