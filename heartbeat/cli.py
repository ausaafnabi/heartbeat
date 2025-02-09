import http.server
import json
import os
import urllib.parse
from heartbeat.server import HeartbeatServer,monitor_heartbeat
import threading
import argparse

def main():
    parser = argparse.ArgumentParser(description='Heartbeat Server')
    parser.add_argument('--folder', type=str, help='Path to the folder where the health check data is stored')
    parser.add_argument('--webhook', type=str, help='Webhook URL for notifications')
    parser.add_argument('--port', type=int, default=8000, help='Port number for the HTTP server')
    args = parser.parse_args()
    if args.folder:
        server_address = ('', args.port)
        server = HeartbeatServer(server_address, args.folder, args.webhook)
        print(f'Server started on port {args.port}')
        threading.Thread(target=monitor_heartbeat, args=(args.folder, args.webhook)).start()
        server.serve_forever()
    else:
        print('Please provide --folder flag')
if __name__ == '__main__':
    main()