import multiprocessing
import requests
import threading
import time
from heartbeat.healthcheck import HealthCheck
from heartbeat.builder import SchemaBuilder

class Query:
    def __init__(self, urls,schema_builder, timeout=5):
        self.urls = urls
        self.timeout = timeout
        self.schema = schema_builder

    def check_url(self, url):
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                self.schema.schema['querystatus']=response.status_code
                return f'{url} is up'
            else:
                return f'{url} returned {response.status_code}'
        except requests.exceptions.RequestException as e:
            return f'{url} is down ({e})'
        time.sleep(5)

    def run_query_check(self):
        with multiprocessing.Pool() as pool:
            results = pool.map(self.check_url, self.urls)
            time.sleep(15)
            return results

if __name__ == '__main__':
    folder_location = './'
    schema_builder = SchemaBuilder("queryservers")
    schema_builder.add_field("querystatus", "int", 400)
    health_check = HealthCheck(folder_location, schema_builder)
    health_check_thread = threading.Thread(target=health_check.update_health_check)
    health_check_thread.daemon = True
    health_check_thread.start()
    # while True:
    #     print(f'Health: {health_check.get_schema_from_file()["health"]}, Liveliness: {health_check.get_liveliness()}')
    #     time.sleep(1)

    urls = [
        'https://example.com',
        'https://google.com',
        'https://github.com',
        'https://www.python.org',
    ]

    query_res = Query(urls,schema_builder)
    start_time = time.time()
    results = query_res.run_query_check()
    
    end_time = time.time()

    for result in results:
        print(result)
    # health_check_thread.join()
    print(f'Health check completed in {end_time - start_time} seconds')