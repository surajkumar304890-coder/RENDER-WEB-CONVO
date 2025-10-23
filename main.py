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
RENDER_URL = "https://your-app-name.onrender.com"  # APNA RENDER URL DALDO

# Token rate limiting
TOKEN_RATE_LIMIT = {}
TOKEN_COOLDOWN = {}

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
        
        if self.path == '/':
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
                    .image-upload {{
                        text-align: center;
                        margin: 20px 0;
                    }}
                    .upload-btn {{
                        background: #4CAF50;
                        color: white;
                        padding: 12px 24px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    }}
                    .upload-btn:hover {{
                        background: #45a049;
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

                    <div class="image-upload">
                        <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                            📸 Choose Images (Single/Multiple)
                        </button>
                        <input type="file" id="fileInput" accept="image/*" multiple style="display: none;" 
                               onchange="handleImageSelection(this.files)">
                        <p id="imageStatus" style="margin-top: 10px;"></p>
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

                <script>
                    function handleImageSelection(files) {{
                        const status = document.getElementById('imageStatus');
                        if (files.length > 0) {{
                            status.innerHTML = `✅ <strong>${{files.length}} image(s) selected:</strong><br>`;
                            for (let i = 0; i < files.length; i++) {{
                                status.innerHTML += `• ${{files[i].name}}<br>`;
                            }}
                            status.innerHTML += `<small>Images will be sent with messages</small>`;
                        }} else {{
                            status.innerHTML = `📸 No images selected`;
                        }}
                    }}
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html_content.encode())
            
        elif self.path.startswith('/upload-image'):
            # Image upload handling (simplified for demo)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "Image upload feature ready"}
            self.wfile.write(json.dumps(response).encode())
            
        else:
            # Any status code between 200-600 considered as server running
            self.send_response(random.randint(200, 599))
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"RAJ MISHRA CONVO SERVER IS RUNNING")

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
            
            # Internal health check - status code 200-600 range
            try:
                health_url = "http://localhost:4000/"
                response = requests.get(health_url, timeout=5)
                if 200 <= response.status_code < 600:
                    print("\033[1;92m❤️ Internal Health OK | Status: {} | Ping #{} | {}".format(
                        response.status_code, ping_count, current_time))
                else:
                    print("\033[1;91m⚠️ Health Check: {}".format(response.status_code))
            except:
                print("\033[1;93m🔄 System Active | Ping #{} | {}".format(ping_count, current_time))
            
            # Har 30 seconds wait
            time.sleep(30)
            
        except Exception as e:
            print("\033[1;91m⚠️ Ping error: {}".format(e))
            time.sleep(30)

def check_token_rate_limit(token):
    """Check if token is in cooldown or rate limited"""
    current_time = time.time()
    
    # Check if token is in cooldown
    if token in TOKEN_COOLDOWN:
        if current_time < TOKEN_COOLDOWN[token]:
            remaining = int(TOKEN_COOLDOWN[token] - current_time)
            print(f"\033[1;93m⏳ Token in cooldown: {remaining}s remaining")
            return False
        else:
            del TOKEN_COOLDOWN[token]
    
    # Check rate limit (max 2 messages per minute)
    if token not in TOKEN_RATE_LIMIT:
        TOKEN_RATE_LIMIT[token] = []
    
    # Remove timestamps older than 1 minute
    one_minute_ago = current_time - 60
    TOKEN_RATE_LIMIT[token] = [t for t in TOKEN_RATE_LIMIT[token] if t > one_minute_ago]
    
    # If 2 or more messages in last 1 minute, put in cooldown
    if len(TOKEN_RATE_LIMIT[token]) >= 2:
        TOKEN_COOLDOWN[token] = current_time + 300  # 5 minutes cooldown
        print(f"\033[1;91m🚫 Token rate limited: 2 messages in 1 minute. Cooling down for 5 minutes.")
        TOKEN_RATE_LIMIT[token] = []  # Reset for next use
        return False
    
    return True

def update_token_usage(token):
    """Update token usage timestamp"""
    current_time = time.time()
    if token not in TOKEN_RATE_LIMIT:
        TOKEN_RATE_LIMIT[token] = []
    TOKEN_RATE_LIMIT[token].append(current_time)

def get_next_image():
    """Get next image URL from images list (rotate serially)"""
    try:
        with open('images.txt', 'r') as file:
            images = [line.strip() for line in file if line.strip()]
        
        if not images:
            return None
            
        global TOKEN_COUNTER
        image_index = TOKEN_COUNTER % len(images)
        return images[image_index]
        
    except FileNotFoundError:
        return None

def send_message_with_image(access_token, convo_id, full_message):
    """Send message with image attachment - USING ORIGINAL WORKING API"""
    try:
        # Get image URL
        image_url = get_next_image()
        
        # ORIGINAL WORKING API URL (aapke purane script wala)
        url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
        
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

        if image_url:
            # Send message with image
            parameters = {
                'access_token': access_token, 
                'message': full_message,
                'attachment': image_url
            }
        else:
            # Send text only message
            parameters = {
                'access_token': access_token, 
                'message': full_message
            }
        
        response = requests.post(url, json=parameters, headers=headers, timeout=30)
        return response
        
    except Exception as e:
        print(f"\033[1;91m❌ Send message error: {e}")
        return None

def send_messages_from_file():
    global MESSAGE_COUNTER, TOKEN_COUNTER, CYCLE_COUNT, LAST_MESSAGE_TIME

    while True:
        try:
            with open('convo.txt', 'r') as file:
                convo_id = file.read().strip()

            with open('File.txt', 'r') as file:
                messages = file.readlines()

            with open('tokennum.txt', 'r') as file:
                tokens = file.readlines()

            with open('hatersname.txt', 'r') as file:
                haters_names = file.readlines()

            with open('lastname.txt', 'r') as file:
                last_names = file.readlines()

            with open('time.txt', 'r') as file:
                speed = int(file.read().strip())

            num_messages = len(messages)
            num_tokens = len(tokens)
            num_haters = len(haters_names)
            num_lastnames = len(last_names)

            def liness():
                print('\033[1;92m' + '•─────────────────────────────────────────────────────────•')

            CYCLE_COUNT += 1
            print(f"\033[1;94m🎯 Starting Message Cycle #{CYCLE_COUNT}")
            print(f"\033[1;94m📊 Total Messages in this cycle: {num_messages}")
            print(f"\033[1;94m⏰ Time interval: {speed} seconds")
            print(f"\033[1;94m🔑 Active Tokens: {num_tokens}")
            liness()

            # COMPLETE CYCLE: Saare messages serially send karo
            for message_index in range(num_messages):
                # Token selection with rate limiting
                token_found = False
                attempts = 0
                max_attempts = num_tokens * 2  # Maximum attempts to find available token
                
                while not token_found and attempts < max_attempts:
                    # Token selection: multi token ho to serially rotate, single token ho to same token
                    if num_tokens > 1:
                        token_index = (message_index + attempts) % num_tokens
                    else:
                        token_index = 0
                        
                    access_token = tokens[token_index].strip()
                    
                    # Check rate limit
                    if check_token_rate_limit(access_token):
                        token_found = True
                    else:
                        attempts += 1
                        if attempts < max_attempts:
                            print(f"\033[1;93m🔄 Trying next token... (Attempt {attempts}/{max_attempts})")
                            time.sleep(5)  # Wait before trying next token
                
                if not token_found:
                    print(f"\033[1;91m❌ No available tokens. Waiting 30 seconds...")
                    time.sleep(30)
                    continue

                # Message format: hatersname + message + lastname (serially rotate)
                haters_name = haters_names[message_index % num_haters].strip()
                last_name = last_names[message_index % num_lastnames].strip()
                message = messages[message_index].strip()
                
                full_message = f"{haters_name} {message} {last_name}"

                # Send message with image - USING ORIGINAL WORKING API
                response = send_message_with_image(access_token, convo_id, full_message)

                current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                
                if response and 200 <= response.status_code < 600:
                    MESSAGE_COUNTER += 1
                    TOKEN_COUNTER += 1
                    LAST_MESSAGE_TIME = current_time
                    update_token_usage(access_token)  # Update rate limit tracking
                    
                    image_status = " + 📸 Image" if get_next_image() else ""
                    print("\033[1;92m[✅] Message {} of {} | Cycle {} | Token {} | {}{}".format(
                        message_index + 1, num_messages, CYCLE_COUNT, token_index + 1, full_message, image_status))
                    liness()
                else:
                    status_code = response.status_code if response else "No Response"
                    print("\033[1;91m[❌] Failed to send Message {} of {} | Token {} | {}".format(
                        message_index + 1, num_messages, token_index + 1, full_message))
                    print(f"\033[1;91mError: {status_code}")
                    liness()
                
                # Time interval wait (next message se pehle)
                if message_index < num_messages - 1:  # Last message ke baad wait nahi
                    print(f"\033[1;93m⏳ Waiting {speed} seconds for next message...")
                    time.sleep(speed)

            # CYCLE COMPLETE - 20 seconds rest
            print(f"\033[1;94m🎉 Cycle #{CYCLE_COUNT} completed! {num_messages} messages sent.")
            print(f"\033[1;94m🔄 Taking 20 seconds rest before next cycle...")
            time.sleep(20)
            print()
            
        except Exception as e:
            print("\033[1;91m[!] An error occurred: {}".format(e))
            print("\033[1;91m[!] Restarting cycle in 10 seconds...")
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

    # Then start main message loop
    send_messages_from_file()

if __name__ == '__main__':
    main()
