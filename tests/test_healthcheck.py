import pytest
import os
import json
from heartbeat.healthcheck import HealthCheck
from heartbeat.schema_builder import SchemaBuilder
import time
import threading

@pytest.fixture
def health_check():
    folder_location = '/tmp/healthcheck'
    schema_builder = SchemaBuilder("my_schema")
    schema_builder.add_field("custom_field", "str", "default_value")
    health_check = HealthCheck(folder_location, schema_builder)
    yield health_check
    if os.path.exists(health_check.folder_location):
        import shutil
        shutil.rmtree(health_check.folder_location)

def test_update_health_check(health_check):
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    time.sleep(1)
    assert os.path.exists(health_check.file_path)
    with open(health_check.file_path, 'r') as f:
        data = json.load(f)
        assert data['health']

def test_get_schema_from_file(health_check):
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    time.sleep(1)
    data = health_check.get_schema_from_file()
    assert data['health']

def test_get_liveliness(health_check):
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    time.sleep(1)
    assert health_check.get_liveliness()

def test_update_health_check_exception(health_check):
    health_check.schema_builder.schema['health'] = 'invalid'
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    time.sleep(1)
    assert os.path.exists(health_check.file_path)
    with open(health_check.file_path, 'r') as f:
        data = json.load(f)
        assert not data['health']

def test_get_schema_from_file_exception(health_check):
    health_check.schema_builder.schema['health'] = 'invalid'
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    time.sleep(1)
    data = health_check.get_schema_from_file()
    assert not data['health']

def test_get_liveliness_exception(health_check):
    health_check.schema_builder.schema['health'] = 'invalid'
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    time.sleep(1)
    assert not health_check.get_liveliness()
