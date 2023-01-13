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


class Collector:
    
    def __init__(self, testbed_filename, command):
        
        from pyats.topology import loader
        
        self.command = command
        self.testbed = loader.load(testbed_filename)
  
    def parse_all_devices(self):

        print("Retrieving data from devices ...")

        output_all_devices = []
        failed_devices = []

        for device in self.testbed.devices.values():

            try:
                print(f"Executing command: {self.command} for device :{device.name}")
                device.connect(init_exec_commands=[], init_config_commands=[], learn_hostname=True, log_stdout=False)
                output = device.parse(self.command)
                output_all_devices.append({device.name : output})

            except Exception as e:
                print(f"Exception -{e}: Execution of command: {self.command} for device: {device.name} failed")
                failed_devices.append(device)

            device.disconnect()

        if failed_devices:
            print("Summary: Execution for the following devices failed:")
            print(failed_devices)

        else:
            print(f"Summary: All devices were parsed successfully for command: {self.command}")

        return output_all_devices