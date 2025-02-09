import os
import json
import time
import asyncio
from typing import Dict
from datetime import datetime
import threading
from heartbeat.builder import SchemaBuilder

class HealthCheck:
    def __init__(self, folder_location: str, schema_builder: SchemaBuilder, interval: int = 10, filename: str = None):
        self.folder_location = folder_location
        self.schema_builder = schema_builder
        self.interval = interval
        self.filename = filename if filename else f'beat_{schema_builder.name}.json'
        self.file_path = os.path.join(folder_location, self.filename)
        self.lock = threading.Lock()
        self.liveliness = True

    def update_health_check(self):
        previous_extra_values = {}
        while True:
            try:
                print(f'Pinged Healthcheck at: {datetime.now().isoformat()}')
                self.schema_builder.schema["health"] = True
                self.schema_builder.schema["last_updated"] = datetime.now().isoformat()
                self.schema_builder.schema["error"] = None
                self.liveliness = True
                self._write_schema_to_file()
                extra_values = {key: value for key, value in self.schema_builder.schema.items() if key not in ["health", "last_updated", "error"]}
            
                # Update the extra values in the health check if they have changed
                if extra_values != previous_extra_values:
                    previous_extra_values = extra_values
                    for key, value in extra_values.items():
                        self.schema_builder.schema[key] = value
                    
                self._write_schema_to_file()
            except Exception as e:
                self.schema_builder.schema["health"] = False
                self.schema_builder.schema["last_updated"] = datetime.now().isoformat()
                self.schema_builder.schema["error"] = str(e)
                self.liveliness = False
                
                # Get the extra values from the schema builder
                extra_values = {key: value for key, value in self.schema_builder.schema.items() if key not in ["health", "last_updated", "error"]}
                
                # Update the extra values in the health check if they have changed
                if extra_values != previous_extra_values:
                    previous_extra_values = extra_values
                    for key, value in extra_values.items():
                        self.schema_builder.schema[key] = value
            time.sleep(self.interval)

    def _write_schema_to_file(self):
        with self.lock:
            if not os.path.exists(self.folder_location):
                os.makedirs(self.folder_location)
            with open(self.file_path, "w") as f:
                json.dump(self.schema_builder.schema, f)

    def get_schema_from_file(self):
        with self.lock:
            if not os.path.exists(self.file_path):
                return {}
            with open(self.file_path, "r") as f:
                return json.load(f)

    def get_liveliness(self):
        return self.liveliness

def main():
    folder_location = '/path/to/folder'
    schema_builder = SchemaBuilder("my_schema")
    schema_builder.add_field("custom_field", "str", "default_value")
    health_check = HealthCheck(folder_location, schema_builder)
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    while True:
        print(f'Health: {health_check.get_schema_from_file()["health"]}, Liveliness: {health_check.get_liveliness()}')
        time.sleep(1)

# if __name__ == "__main__":
#     main()


# class HealthCheck:
#     def __init__(self, file_path: str, schema_builder: SchemaBuilder, interval: int = 10):
#         """
#         Initialize the HealthCheck class.

#         Args:
#         - file_path (str): The path to the file where the health check data will be stored.
#         - schema_builder (SchemaBuilder): The schema builder instance.
#         - interval (int): The interval in seconds at which the health check data will be updated.
#         """
#         self.file_path = file_path
#         self.schema_builder = schema_builder
#         self.interval = interval
#         self.lock = asyncio.Lock() if asyncio.get_event_loop() else None

#     async def update_health_check(self):
#         """
#         Update the health check data in the file.

#         This method is designed to be run in an async context.
#         """
#         while True:
#             try:
#                 # Simulate a health check
#                 self.schema_builder.schema["health"] = True
#                 self.schema_builder.schema["last_updated"] = int(time.time())
#                 self.schema_builder.schema["error"] = None
#                 async with self.lock:
#                     self._write_schema_to_file()
#             except Exception as e:
#                 self.schema_builder.schema["health"] = False
#                 self.schema_builder.schema["last_updated"] = int(time.time())
#                 self.schema_builder.schema["error"] = str(e)
#                 async with self.lock:
#                     self._write_schema_to_file()
#             await asyncio.sleep(self.interval)

#     def _write_schema_to_file(self):
#         """
#         Write the schema to the file.
#         """
#         if not os.path.exists(self.file_path):
#             with open(self.file_path, "w") as f:
#                 json.dump({}, f)
#         with open(self.file_path, "r+") as f:
#             data = json.load(f)
#             data[self.schema_builder.name] = self.schema_builder.schema
#             f.seek(0)
#             json.dump(data, f)
#             f.truncate()

#     def start_async(self):
#         """
#         Start the health check in an async context.
#         """
#         loop = asyncio.get_event_loop()
#         loop.create_task(self.update_health_check())
#         loop.run_forever()

