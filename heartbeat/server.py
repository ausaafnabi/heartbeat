import http.server
import json
import os
import urllib.parse
import requests
import threading
import time

class HeartbeatServer(http.server.HTTPServer):
    def __init__(self, server_address, folder_location, webhook_url):
        self.folder_location = folder_location
        self.webhook_url = webhook_url
        super().__init__(server_address, RequestHandler)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/heartbeat':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            heartbeat_data = self.get_heartbeat_data()
            self.wfile.write(json.dumps(heartbeat_data).encode())
        elif parsed_path.path == '/liveliness':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            liveliness_data = self.get_liveliness_data()
            self.wfile.write(json.dumps(liveliness_data).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def get_heartbeat_data(self):
        heartbeat_data = {}
        for root, dirs, files in os.walk(self.server.folder_location):
            for file in files:
                if file.startswith('beat_') and file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        heartbeat_data[file] = data
        return heartbeat_data

    def get_liveliness_data(self):
        liveliness_data = {}
        for root, dirs, files in os.walk(self.server.folder_location):
            for file in files:
                if file.startswith('beat_') and file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        if data['health']:
                            liveliness_data[file] = 'alive'
                        else:
                            liveliness_data[file] = 'not alive'
        return liveliness_data

    def log_message(self, format, *args):
        pass

def send_webhook_notification(webhook_url, data):
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code != 200:
            print(f'Failed to send webhook notification: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to send webhook notification: {e}')

def monitor_heartbeat(folder_location, webhook_url):
    while True:
        for root, dirs, files in os.walk(folder_location):
            for file in files:
                if file.startswith('beat_') and file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        if not data['health']:
                            send_webhook_notification(webhook_url, {'file': file, 'status': 'not alive'})
        time.sleep(60)

def main():
    folder_location = '/path/to/folder'
    webhook_url = 'https://example.com/webhook'
    server_address = ('', 8000)
    server = HeartbeatServer(server_address, folder_location, webhook_url)
    print(f'Server started on port 8000')
    threading.Thread(target=monitor_heartbeat, args=(folder_location, webhook_url)).start()
    server.serve_forever()

if __name__ == '__main__':
    main()

