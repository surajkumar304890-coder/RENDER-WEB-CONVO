import requests
import time
import threading
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

print("🚀 RAJ MISHRA CONVO SERVER STARTING...")

# Global variables
MESSAGE_COUNTER = 0
TOKEN_COUNTER = 0
CYCLE_COUNT = 0
LAST_MESSAGE_TIME = None
START_TIME = datetime.now()
RENDER_URL = "https://manu-tyagi-vs-veer-daksh-20-oct-2025.onrender.com"  # YAHI APNA RENDER URL DALDO

class HealthHandler(BaseHTTPRequestHandler):
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
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "running",
                "service": "facebook_messenger_bot",
                "message": "RAJ MISHRA CONVO SERVER IS RUNNING",
                "render_url": RENDER_URL,
                "started_time": START_TIME.strftime('%d/%m/%Y %I:%M:%S %p IST'),
                "current_time": indian_time,
                "uptime": f"{months}M {days}D {hours}H {minutes}M {seconds}S",
                "messages_sent": MESSAGE_COUNTER,
                "cycles_completed": CYCLE_COUNT,
                "last_activity": LAST_MESSAGE_TIME
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/send-now':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                result = send_single_message()
                response = {
                    "status": "success" if result else "failed",
                    "message": "Manual message sent" if result else "Failed to send message",
                    "timestamp": indian_time
                }
            except Exception as e:
                response = {"status": "error", "message": str(e)}
                
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def run_health_server():
    """Port 4000 pe health server chalta hai"""
    try:
        server = HTTPServer(('0.0.0.0', 4000), HealthHandler)
        print("✅ Health Server Started: Port 4000")
        print(f"🌐 Render URL: {RENDER_URL}")
        print("🕒 Real-time Uptime Counter Activated")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Health server error: {e}")

def load_config():
    """Configuration files load karta hai"""
    try:
        config = {}
        
        with open('token.txt', 'r') as f:
            config['tokens'] = [line.strip() for line in f if line.strip()]
        
        with open('convo.txt', 'r') as f:
            config['group_id'] = f.read().strip()
        
        with open('time.txt', 'r') as f:
            config['interval'] = int(f.read().strip())
        
        with open('hatersname.txt', 'r') as f:
            config['names'] = [line.strip() for line in f if line.strip()]
        
        with open('lastname.txt', 'r') as f:
            config['lastnames'] = [line.strip() for line in f if line.strip()]
        
        with open('message.txt', 'r') as f:
            config['messages'] = [line.strip() for line in f if line.strip()]
        
        print(f"✅ Config loaded: {len(config['tokens'])} tokens, {len(config['messages'])} messages")
        return config
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return None

def send_single_message():
    """Single message send karta hai with correct Facebook API"""
    global MESSAGE_COUNTER, TOKEN_COUNTER, LAST_MESSAGE_TIME
    
    try:
        config = load_config()
        if not config:
            return False
        
        # Current token and message select karo
        token = config['tokens'][TOKEN_COUNTER % len(config['tokens'])]
        name = config['names'][MESSAGE_COUNTER % len(config['names'])]
        lastname = config['lastnames'][MESSAGE_COUNTER % len(config['lastnames'])]
        message_text = config['messages'][MESSAGE_COUNTER % len(config['messages'])]
        
        full_message = f"{name} {message_text} {lastname}"
        
        # CORRECT Facebook API URL for groups
        url = f"https://graph.facebook.com/v17.0/{config['group_id']}/messages"
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        payload = {
            'message': full_message,
            'access_token': token
        }
        
        print(f"📤 Sending: {full_message[:60]}...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            MESSAGE_COUNTER += 1
            TOKEN_COUNTER += 1
            LAST_MESSAGE_TIME = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p IST')
            print(f"✅ Message {MESSAGE_COUNTER} sent successfully! | {LAST_MESSAGE_TIME}")
            return True
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Send error: {e}")
        return False

def internal_self_ping():
    """Render ke liye internal self-ping system"""
    ping_count = 0
    while True:
        try:
            ping_count += 1
            current_time = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p IST')
            
            # Internal health check - apne aap ko check karega
            try:
                health_url = "http://localhost:4000/health"
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"❤️ Internal Health OK | Ping #{ping_count} | {current_time}")
                else:
                    print(f"⚠️ Health Check: {response.status_code}")
            except:
                print(f"🔄 System Active | Ping #{ping_count} | {current_time}")
            
            # Har 30 seconds wait (Render URL ko ping karega)
            try:
                # External Render URL ko bhi ping karega
                if ping_count % 2 == 0:  # Har doosri ping pe
                    external_response = requests.get(RENDER_URL, timeout=10)
                    print(f"🌐 External Ping to {RENDER_URL} | Status: {external_response.status_code}")
            except Exception as e:
                print(f"🌐 External Ping Failed: {e}")
            
            # Har 30 seconds wait
            time.sleep(30)
            
        except Exception as e:
            print(f"⚠️ Ping error: {e}")
            time.sleep(30)

def start_messaging_cycle():
    """Main messaging cycle - files ke according kaam karega"""
    global CYCLE_COUNT, MESSAGE_COUNTER
    
    print("🔄 Starting messaging cycle...")
    
    # Initial 15 second wait
    print("⏳ Initial 15 second wait...")
    time.sleep(15)
    
    # First message immediately after 15 seconds
    print("🚀 Sending first message after initial wait...")
    send_single_message()
    
    while True:
        try:
            CYCLE_COUNT += 1
            print(f"\n🎯 Starting Cycle #{CYCLE_COUNT}")
            print("=" * 50)
            
            config = load_config()
            if not config:
                print("❌ Config missing, retrying in 30 seconds...")
                time.sleep(30)
                continue
            
            # Har message ke beich configured interval wait karo
            interval = config['interval']
            total_messages = len(config['messages'])
            
            for i in range(total_messages):
                if i > 0:  # First message already sent
                    print(f"⏳ Waiting {interval} seconds for next message...")
                    time.sleep(interval)
                
                success = send_single_message()
                
                if not success:
                    print("❄️ Cooling down after error...")
                    time.sleep(10)
            
            # Cycle complete - 20 seconds rest
            print(f"🎉 Cycle #{CYCLE_COUNT} completed! Taking 20 seconds rest...")
            time.sleep(20)
            
        except Exception as e:
            print(f"❌ Cycle error: {e}")
            print("🔄 Restarting cycle in 10 seconds...")
            time.sleep(10)

def main():
    print("=" * 60)
    print("🤖 RAJ MISHRA FACEBOOK MESSENGER BOT")
    print("🌐 Non-Stop Render Free Plan")
    print("🕒 Real-time Uptime Counter")
    print(f"🌐 Render URL: {RENDER_URL}")
    print("=" * 60)
    
    # Health server start
    server_thread = threading.Thread(target=run_health_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Internal ping system start
    ping_thread = threading.Thread(target=internal_self_ping, daemon=True)
    ping_thread.start()
    
    # Messaging cycle start
    start_messaging_cycle()

if __name__ == "__main__":
    main()
