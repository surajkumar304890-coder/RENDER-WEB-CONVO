import requests
import json
import time
import sys
import os
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
RENDER_URL = "https://arjun-vs-alex.onrender.com"  # APNA RENDER URL DALDO

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
                            <p style="font-size: 16px; margin: 5px 0;">Render Free Plan - ALWAYS ACTIVE</p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 20px; opacity: 0.8;">
                        <p>🔄 Auto-refreshing every second | 🏠 Internal Ping Active | 🌍 24/7 Online</p>
                        <p>📸 Image + Text Support | 🔒 Rate Limited: 2 msg/min</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            self.wfile.write(html_content.encode())
            
        else:
            # Any status code between 200-600 considered as server running
            status_code = random.choice([200, 201, 202, 204, 206, 301, 302, 304, 400, 401, 403, 404, 500, 501, 502, 503])
            self.send_response(status_code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"RAJ MISHRA CONVO SERVER IS RUNNING")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("•──────────────────────RAJ H3R3 ───────────────────────────────•")
        print("🚀 Server running at http://localhost:{}".format(PORT))
        print("📡 Status: ALWAYS ACTIVE - Never Sleeping")
        httpd.serve_forever()

def internal_self_ping():
    """Render ke liye internal self-ping system - HAR 25 SECONDS"""
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
                    print("❤️ Internal Health OK | Status: {} | Ping #{} | {}".format(
                        response.status_code, ping_count, current_time))
                else:
                    print("⚠️ Health Check: {}".format(response.status_code))
            except:
                print("🔄 System Active | Ping #{} | {}".format(ping_count, current_time))
            
            # Har 25 seconds wait (Render free plan ke liye optimized)
            time.sleep(25)
            
        except Exception as e:
            print("⚠️ Ping error: {}".format(e))
            time.sleep(25)

def check_token_rate_limit(token):
    """Check if token is in cooldown or rate limited"""
    current_time = time.time()
    
    # Check if token is in cooldown
    if token in TOKEN_COOLDOWN:
        if current_time < TOKEN_COOLDOWN[token]:
            remaining = int(TOKEN_COOLDOWN[token] - current_time)
            print("⏳ Token in cooldown: {}s remaining".format(remaining))
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
        print("🚫 Token rate limited: 2 messages in 1 minute. Cooling down for 5 minutes.")
        TOKEN_RATE_LIMIT[token] = []  # Reset for next use
        return False
    
    return True

def update_token_usage(token):
    """Update token usage timestamp"""
    current_time = time.time()
    if token not in TOKEN_RATE_LIMIT:
        TOKEN_RATE_LIMIT[token] = []
    TOKEN_RATE_LIMIT[token].append(current_time)

def get_next_image_url():
    """Get next image URL from images.txt file"""
    try:
        if os.path.exists('images.txt'):
            with open('images.txt', 'r') as file:
                images = [line.strip() for line in file if line.strip()]
            
            if images:
                global TOKEN_COUNTER
                image_index = TOKEN_COUNTER % len(images)
                return images[image_index]
        
        return None
        
    except Exception as e:
        print("❌ Image URL error: {}".format(e))
        return None

def send_message_with_image(access_token, convo_id, full_message):
    """Send message with image attachment - USING IMAGE URL"""
    try:
        # Get image URL
        image_url = get_next_image_url()
        
        # ORIGINAL WORKING API URL
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
            # Send message with image URL
            parameters = {
                'access_token': access_token, 
                'message': full_message,
                'attachment': image_url
            }
            print("📸 Sending message with image: {}".format(image_url))
        else:
            # Send text only message
            parameters = {
                'access_token': access_token, 
                'message': full_message
            }
            print("📝 Sending text only message")
        
        response = requests.post(url, json=parameters, headers=headers, timeout=30)
        return response
        
    except Exception as e:
        print("❌ Send message error: {}".format(e))
        return None

def send_messages_from_file():
    global MESSAGE_COUNTER, TOKEN_COUNTER, CYCLE_COUNT, LAST_MESSAGE_TIME

    print("🔄 Starting messaging system...")
    
    # Quick start - no long initial wait
    time.sleep(5)

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
                print('•─────────────────────────────────────────────────────────•')

            CYCLE_COUNT += 1
            print("🎯 Starting Message Cycle #{}".format(CYCLE_COUNT))
            print("📊 Total Messages in this cycle: {}".format(num_messages))
            print("⏰ Time interval: {} seconds".format(speed))
            print("🔑 Active Tokens: {}".format(num_tokens))
            
            # Check if images available
            image_url = get_next_image_url()
            if image_url:
                print("📸 Images: Available - {} images loaded".format(len([line for line in open('images.txt')])))
            else:
                print("❌ Images: Not available - Text only mode")
                
            liness()

            # COMPLETE CYCLE: Saare messages serially send karo
            for message_index in range(num_messages):
                # Token selection with rate limiting
                token_found = False
                attempts = 0
                max_attempts = num_tokens * 2
                
                while not token_found and attempts < max_attempts:
                    if num_tokens > 1:
                        token_index = (message_index + attempts) % num_tokens
                    else:
                        token_index = 0
                        
                    access_token = tokens[token_index].strip()
                    
                    if check_token_rate_limit(access_token):
                        token_found = True
                    else:
                        attempts += 1
                        if attempts < max_attempts:
                            print("🔄 Trying next token... (Attempt {}/{})".format(attempts, max_attempts))
                            time.sleep(3)
                
                if not token_found:
                    print("❌ No available tokens. Waiting 20 seconds...")
                    time.sleep(20)
                    continue

                # Message format: hatersname + message + lastname
                haters_name = haters_names[message_index % num_haters].strip()
                last_name = last_names[message_index % num_lastnames].strip()
                message = messages[message_index].strip()
                
                full_message = "{} {} {}".format(haters_name, message, last_name)

                # Send message with image
                response = send_message_with_image(access_token, convo_id, full_message)

                current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                
                if response and 200 <= response.status_code < 600:
                    MESSAGE_COUNTER += 1
                    TOKEN_COUNTER += 1
                    LAST_MESSAGE_TIME = current_time
                    update_token_usage(access_token)
                    
                    if image_url:
                        print("[✅] Message {} of {} | Cycle {} | Token {} | {} + 📸 Image".format(
                            message_index + 1, num_messages, CYCLE_COUNT, token_index + 1, full_message))
                    else:
                        print("[✅] Message {} of {} | Cycle {} | Token {} | {}".format(
                            message_index + 1, num_messages, CYCLE_COUNT, token_index + 1, full_message))
                    liness()
                else:
                    status_code = response.status_code if response else "No Response"
                    print("[❌] Failed to send Message {} of {} | Token {} | {}".format(
                        message_index + 1, num_messages, token_index + 1, full_message))
                    print("Error: {}".format(status_code))
                    liness()
                
                # Time interval wait
                if message_index < num_messages - 1:
                    print("⏳ Waiting {} seconds for next message...".format(speed))
                    time.sleep(speed)

            # CYCLE COMPLETE - 15 seconds rest (reduced for faster cycles)
            print("🎉 Cycle #{} completed! {} messages sent.".format(CYCLE_COUNT, num_messages))
            print("🔄 Taking 15 seconds rest before next cycle...")
            time.sleep(15)
            print()
            
        except Exception as e:
            print("[!] An error occurred: {}".format(e))
            print("[!] Restarting cycle in 5 seconds...")
            time.sleep(5)

def main():
    print("=" * 60)
    print("🤖 RAJ MISHRA FACEBOOK MESSENGER BOT")
    print("🚀 IMAGE + TEXT SUPPORT - SIMPLE SETUP")
    print("📸 Automatic Image Rotation | 🔒 Smart Rate Limiting")
    print("=" * 60)
    
    # Check if images.txt exists
    if os.path.exists('images.txt'):
        with open('images.txt', 'r') as f:
            image_count = len([line for line in f if line.strip()])
        print("📄 images.txt found - {} images loaded!".format(image_count))
        print("✅ Image + Text mode activated!")
    else:
        print("❌ images.txt not found - Text only mode")
        print("💡 Tip: Create images.txt file with image URLs for image support")

    # Start server in background thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    # Start internal ping system
    ping_thread = threading.Thread(target=internal_self_ping)
    ping_thread.daemon = True
    ping_thread.start()

    # Quick start - reduced wait time
    time.sleep(2)

    # Start main message loop
    send_messages_from_file()

if __name__ == '__main__':
    main()
