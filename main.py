import requests
import json
import time
import sys
from platform import system
import os
import subprocess
import http.server
import socketserver
import threading
import random
from datetime import datetime

# Global variables for monitoring
MESSAGE_COUNTER = 0
TOKEN_COUNTER = 0
CYCLE_COUNT = 0
LAST_MESSAGE_TIME = None
START_TIME = datetime.now()
RENDER_URL = "https://raj-testing-20-oct-25.onrender.com"  # APNA RENDER URL DALDO

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global LAST_MESSAGE_TIME, MESSAGE_COUNTER, CYCLE_COUNT, START_TIME
        
        # Calculate uptime
        current_time = datetime.now()
        uptime_delta = current_time - START_TIME
        uptime_seconds = int(uptime_delta.total_seconds())
        
        # Convert to months, days, hours, minutes, seconds
        months = uptime_seconds // (30 * 24 * 3600)
        uptime_seconds %= (30 * 24 * 3600)
        days = uptime_seconds // (24 * 3600)
        uptime_seconds %= (24 * 3600)
        hours = uptime_seconds // 3600
        uptime_seconds %= 3600
        minutes = uptime_seconds // 60
        seconds = uptime_seconds % 60
        
        # Indian time in 12-hour format
        indian_time = current_time.strftime('%d/%m/%Y %I:%M:%S %p IST')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RAJ MISHRA CONVO SERVER</title>
            <meta http-equiv="refresh" content="1">
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 20px;
                    color: white;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .status-box {{
                    background: rgba(255,255,255,0.2);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 10px 0;
                }}
                .uptime {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #00ff00;
                    text-align: center;
                    margin: 20px 0;
                }}
                .render-url {{
                    background: #000;
                    color: #00ff00;
                    padding: 10px;
                    border-radius: 5px;
                    font-family: monospace;
                    text-align: center;
                    margin: 15px 0;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin-top: 20px;
                }}
                .stat-item {{
                    background: rgba(0,0,0,0.3);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 RAJ MISHRA CONVO SERVER</h1>
                    <p>Facebook Messenger Automation System</p>
                </div>
                
                <div class="status-box">
                    <h2>🟢 SERVER STATUS: RUNNING</h2>
                    <p><strong>Started:</strong> {START_TIME.strftime('%d/%m/%Y %I:%M:%S %p IST')}</p>
                    <p><strong>Current Time:</strong> {indian_time}</p>
                </div>
                
                <div class="uptime">
                    ⏰ UPTIME: {months} Months {days} Days {hours} Hours {minutes} Minutes {seconds} Seconds
                </div>
                
                <div class="render-url">
                    🌐 MONITOR URL: {RENDER_URL}
                </div>
                
                <div class="stats">
                    <div class="stat-item">
                        <h3>📨 Messages Sent</h3>
                        <p style="font-size: 24px; margin: 5px 0;">{MESSAGE_COUNTER}</p>
                    </div>
                    <div class="stat-item">
                        <h3>🔄 Cycles Completed</h3>
                        <p style="font-size: 24px; margin: 5px 0;">{CYCLE_COUNT}</p>
                    </div>
                    <div class="stat-item">
                        <h3>⚡ Last Activity</h3>
                        <p style="font-size: 16px; margin: 5px 0;">{LAST_MESSAGE_TIME if LAST_MESSAGE_TIME else 'No messages yet'}</p>
                    </div>
                    <div class="stat-item">
                        <h3>🔧 Service Type</h3>
                        <p style="font-size: 16px; margin: 5px 0;">Render Free Plan</p>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 20px; opacity: 0.8;">
                    <p>🔄 Auto-refreshing every second | 🏠 Internal Ping Active | 🌍 24/7 Online</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode())

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("•──────────────────────RAJ H3R3 ───────────────────────────────•")
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def internal_self_ping():
    """Render ke liye internal self-ping system"""
    ping_count = 0
    while True:
        try:
            ping_count += 1
            current_time = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p IST')
            
            # Internal health check
            try:
                health_url = "http://localhost:4000/"
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print("\033[1;92m❤️ Internal Health OK | Ping #{} | {}".format(ping_count, current_time))
                else:
                    print("\033[1;91m⚠️ Health Check: {}".format(response.status_code))
            except:
                print("\033[1;93m🔄 System Active | Ping #{} | {}".format(ping_count, current_time))
            
            # Har 30 seconds wait (Render URL ko ping karega)
            try:
                if ping_count % 2 == 0:  # Har doosri ping pe
                    external_response = requests.get(RENDER_URL, timeout=10)
                    print("\033[1;94m🌐 External Ping to {} | Status: {}".format(RENDER_URL, external_response.status_code))
            except Exception as e:
                print("\033[1;91m🌐 External Ping Failed: {}".format(e))
            
            # Har 30 seconds wait
            time.sleep(30)
            
        except Exception as e:
            print("\033[1;91m⚠️ Ping error: {}".format(e))
            time.sleep(30)

def send_messages_from_file():
    global MESSAGE_COUNTER, TOKEN_COUNTER, CYCLE_COUNT, LAST_MESSAGE_TIME

    while True:
        try:
            with open('convo.txt', 'r') as file:
                convo_id = file.read().strip()

            with open('File.txt', 'r') as file:
                messages = file.readlines()

            num_messages = len(messages)

            with open('tokennum.txt', 'r') as file:
                tokens = file.readlines()
            num_tokens = len(tokens)
            max_tokens = min(num_tokens, num_messages)

            with open('hatersname.txt', 'r') as file:
                haters_names = file.readlines()

            with open('lastname.txt', 'r') as file:
                last_names = file.readlines()

            with open('time.txt', 'r') as file:
                speed = int(file.read().strip())

            def liness():
                print('\033[1;92m' + '•─────────────────────────────────────────────────────────•')

            headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
                'referer': 'www.google.com'
            }

            CYCLE_COUNT += 1
            print(f"\033[1;94m🎯 Starting Message Cycle #{CYCLE_COUNT}")

            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()

                # NEW MESSAGE FORMAT: hatersname + message + lastname
                haters_name = haters_names[message_index % len(haters_names)].strip()
                last_name = last_names[message_index % len(last_names)].strip()
                message = messages[message_index].strip()
                
                full_message = f"{haters_name} {message} {last_name}"

                url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': full_message}
                response = requests.post(url, json=parameters, headers=headers)

                current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                
                if response.ok:
                    MESSAGE_COUNTER += 1
                    TOKEN_COUNTER += 1
                    LAST_MESSAGE_TIME = current_time
                    print("\033[1;92m[+] Han Chla Gya Massage {} of Convo {} Token {}: {}".format(
                        MESSAGE_COUNTER, convo_id, token_index + 1, full_message))
                    liness()
                else:
                    print("\033[1;91m[x] Failed to send Message {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, full_message))
                    liness()
                
                time.sleep(speed)

            print("\033[1;94m\n[+] All messages sent. Restarting the process...\n")
            
        except Exception as e:
            print("\033[1;91m[!] An error occurred: {}".format(e))
            time.sleep(10)

def main():
    # Start server in background thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    # Start internal ping system
    ping_thread = threading.Thread(target=internal_self_ping)
    ping_thread.daemon = True
    ping_thread.start()

    # Wait a bit for server to start
    time.sleep(2)

    # Then start main message loop (INITIAL MESSAGE FUNCTION REMOVED)
    send_messages_from_file()

if __name__ == '__main__':
    main()
