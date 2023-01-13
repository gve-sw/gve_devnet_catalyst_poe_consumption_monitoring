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

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDB:
    
    def __init__(self, influxdb_host, influxdb_port, influxdb_token, influxdb_org, influxdb_bucket, kWh_price):
        
        self.influxdb_host = influxdb_host
        self.influxdb_port = influxdb_port
        self.influxdb_token = influxdb_token
        self.influxdb_org = influxdb_org
        self.influxdb_bucket = influxdb_bucket
        self.client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
        self.kWh_price = kWh_price


    def convert_collector_to_influx_format(self,collector_output):

        print("Converting json in Influx Points...")
        
        influx_data = []
        overall_used_power_watt = 0
        
        for device_data in collector_output:
            
            used_device_power_watt = 0
            device_name = list(device_data.keys())[0]
            interfaces = device_data[device_name]['interface']
            interface_keys = list(interfaces.keys())

            for interface_key in interface_keys:
                
                interface_power = interfaces[interface_key]['power']
                interface_record = Point("poe_usage").tag("device", device_name).tag("interface", interface_key).field("power", interface_power)
                influx_data.append(interface_record)
                
                used_device_power_watt += interface_power

            overall_used_power_watt += used_device_power_watt
            
        energy_costs = overall_used_power_watt/1000 * self.kWh_price/100
        energy_record = Point("poe_usage").field("energy_costs", energy_costs)
        influx_data.append(energy_record)

        return influx_data
        
 
    def syncronous_write(self, records):

        print("Writing Influx Points to InfluxDB ...")

        try:
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.influxdb_bucket, org=self.influxdb_org, record=records)

        except InfluxDBError as e:
            if e.response.status == 401:
                raise Exception(f"Insufficient write permissions to {self.influxdb_bucket}.") from e
            raise
        except Exception as e:
            print(f"Exception: {e}")

