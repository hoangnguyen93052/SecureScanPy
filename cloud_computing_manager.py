import json
import time
import random
import threading
import requests

class Resource:
    def __init__(self, name, resource_type):
        self.name = name
        self.resource_type = resource_type
        self.status = 'stopped'
        self.location = None

    def start(self):
        self.status = 'running'
        print(f"{self.resource_type} '{self.name}' started.")

    def stop(self):
        self.status = 'stopped'
        print(f"{self.resource_type} '{self.name}' stopped.")

class ComputeResource(Resource):
    def __init__(self, name):
        super().__init__(name, 'Compute')
        self.cpu_usage = 0
        self.memory_usage = 0

    def update_usage(self):
        self.cpu_usage = random.randint(0, 100)
        self.memory_usage = random.randint(0, 100)
        print(f"{self.resource_type} '{self.name}' CPU Usage: {self.cpu_usage}%, Memory Usage: {self.memory_usage}%")

class StorageResource(Resource):
    def __init__(self, name):
        super().__init__(name, 'Storage')
        self.capacity_used = 0

    def update_usage(self):
        self.capacity_used = random.randint(0, 100)
        print(f"{self.resource_type} '{self.name}' Storage Used: {self.capacity_used}GB")

class NetworkResource(Resource):
    def __init__(self, name):
        super().__init__(name, 'Network')
        self.bandwidth_used = 0

    def update_usage(self):
        self.bandwidth_used = random.randint(0, 100)
        print(f"{self.resource_type} '{self.name}' Bandwidth Used: {self.bandwidth_used}Mbps")

class CloudManager:
    def __init__(self):
        self.resources = []

    def add_resource(self, resource):
        self.resources.append(resource)
        print(f"Added {resource.resource_type} '{resource.name}' to the cloud manager.")

    def start_resources(self):
        for resource in self.resources:
            resource.start()

    def stop_resources(self):
        for resource in self.resources:
            resource.stop()

    def monitor_resources(self):
        while True:
            for resource in self.resources:
                if resource.status == 'running':
                    if isinstance(resource, ComputeResource):
                        resource.update_usage()
                    elif isinstance(resource, StorageResource):
                        resource.update_usage()
                    elif isinstance(resource, NetworkResource):
                        resource.update_usage()
            time.sleep(5)

class CloudAPI:
    BASE_URL = "http://api.cloudprovider.com/v1/"

    @staticmethod
    def create_instance(instance_data):
        response = requests.post(f"{CloudAPI.BASE_URL}instances", json=instance_data)
        return response.json()

    @staticmethod
    def delete_instance(instance_id):
        response = requests.delete(f"{CloudAPI.BASE_URL}instances/{instance_id}")
        return response.json()

    @staticmethod
    def list_instances():
        response = requests.get(f"{CloudAPI.BASE_URL}instances")
        return response.json()

class CloudUser:
    def __init__(self, username):
        self.username = username
        self.cloud_manager = CloudManager()

    def launch_instance(self, resource_type, name):
        if resource_type == 'compute':
            instance = ComputeResource(name)
        elif resource_type == 'storage':
            instance = StorageResource(name)
        elif resource_type == 'network':
            instance = NetworkResource(name)
        else:
            print("Unknown resource type.")
            return
        self.cloud_manager.add_resource(instance)

    def delete_instance(self, instance_name):
        instance = next((x for x in self.cloud_manager.resources if x.name == instance_name), None)
        if instance:
            self.cloud_manager.resources.remove(instance)
            print(f"{instance.resource_type} '{instance_name}' deleted.")

    def start_all(self):
        self.cloud_manager.start_resources()

    def stop_all(self):
        self.cloud_manager.stop_resources()

    def monitor(self):
        monitoring_thread = threading.Thread(target=self.cloud_manager.monitor_resources)
        monitoring_thread.start()

if __name__ == "__main__":
    user = CloudUser("john_doe")
    user.launch_instance('compute', 'web-server-1')
    user.launch_instance('storage', 'user-data')
    user.launch_instance('network', 'vpc-1')
    
    user.start_all()
    user.monitor()

    time.sleep(20)

    user.stop_all()
    user.delete_instance('web-server-1')
    user.delete_instance('user-data')
    user.delete_instance('vpc-1')