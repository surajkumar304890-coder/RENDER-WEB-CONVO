import requests
import time
import threading
import random
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Simple HTTP Server for Port 4000
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"RAJ MISHRA CONVO SERVER IS RUNNING")
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "running",
                "service": "facebook_messenger_bot", 
                "message": "RAJ MISHRA CONVO SERVER IS RUNNING",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Server logs suppress karta hoon taaki spam na ho
        pass

def run_health_server():
    """Port 4000 pe simple HTTP server chalta hai"""
    try:
        server = HTTPServer(('0.0.0.0', 4000), HealthHandler)
        print("🌐 Health Server Started: Port 4000 | Response: 'RAJ MISHRA CONVO SERVER IS RUNNING'")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Health server error: {e}")

class FacebookMessengerBot:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v17.0"
        self.load_config()
        self.message_counter = 0
        self.token_counter = 0
        self.running = True
        self.cycle_count = 0
        self.total_messages_sent = 0
        
    def load_config(self):
        """सभी configuration files load करता है"""
        try:
            # Token file - serially rotate
            with open('token.txt', 'r') as f:
                self.tokens = [line.strip() for line in f if line.strip()]
            
            # Group thread ID
            with open('convo.txt', 'r') as f:
                self.group_thread_id = f.read().strip()
            
            # Time interval
            with open('time.txt', 'r') as f:
                self.time_interval = int(f.read().strip())
            
            # Names and messages
            with open('hatersname.txt', 'r') as f:
                self.haters_names = [line.strip() for line in f if line.strip()]
            
            with open('lastname.txt', 'r') as f:
                self.last_names = [line.strip() for line in f if line.strip()]
            
            with open('message.txt', 'r') as f:
                self.messages = [line.strip() for line in f if line.strip()]
                
            print(f"✅ Configuration loaded: {len(self.tokens)} tokens, {len(self.messages)} messages")
            
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            self.running = False
    
    def get_current_token(self):
        """Current token serially लेता है"""
        if not self.tokens:
            return None
        token = self.tokens[self.token_counter % len(self.tokens)]
        return token
    
    def get_current_message(self):
        """Current message serially लेता है और format करता है"""
        if not self.messages or not self.haters_names or not self.last_names:
            return None
        
        msg_index = self.message_counter % len(self.messages)
        name_index = self.message_counter % len(self.haters_names)
        last_name_index = self.message_counter % len(self.last_names)
        
        message = f"{self.haters_names[name_index]} {self.messages[msg_index]} {self.last_names[last_name_index]}"
        return message
    
    def rotate_counters(self):
        """Counters को increment करता है"""
        self.message_counter += 1
        self.token_counter += 1
    
    def send_message(self, token, message):
        """Facebook API के through message send करता है"""
        url = f"{self.base_url}/{self.group_thread_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.facebook.com',
            'Referer': 'https://www.facebook.com/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        payload = {
            'message': message,
            'access_token': token
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Message sent successfully | Token: {token[:15]}... | Time: {datetime.now().strftime('%H:%M:%S')}")
                self.total_messages_sent += 1
                return True
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return False

    def betterstack_uptime_monitor(self):
        """BetterStack/UptimeRobot ke liye monitor URL generate karta hai"""
        monitor_count = 0
        while self.running:
            try:
                monitor_count += 1
                
                # BetterStack/UptimeRobot ke liye monitor URL
                print(f"🔔 MONITOR_URL: https://your-app-name.onrender.com")
                print(f"📊 Stats: {self.total_messages_sent} total messages | {self.cycle_count} cycles")
                
                # Health status display karta hai
                print(f"🟢 HEALTHY | RAJ MISHRA CONVO SERVER IS RUNNING | Check #{monitor_count}")
                
                # 5-8 minute wait
                wait_time = random.randint(300, 480)
                for i in range(wait_time):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"⚠️ Monitor error: {e}")
                time.sleep(60)
    
    def keep_alive_ping(self):
        """Script को always active रखने के लिए internal ping"""
        ping_count = 0
        while self.running:
            try:
                ping_count += 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Self-ping to port 4000 - Internal health check
                try:
                    response = requests.get('http://localhost:4000/', timeout=5)
                    if response.status_code == 200:
                        print(f"❤️ Port 4000 Health: OK | {current_time}")
                    else:
                        print(f"⚠️ Port 4000 Health: {response.status_code}")
                except:
                    print(f"🔄 System Active Ping #{ping_count} | {current_time}")
                
                # हर 10 seconds में internal ping
                for i in range(6):
                    if not self.running:
                        break
                    time.sleep(10)
                    
            except Exception as e:
                print(f"⚠️ Ping error: {e}")
                time.sleep(10)
    
    def auto_restart_monitor(self):
        """Automatic restart mechanism अगर script stuck हो जाए"""
        monitor_count = 0
        while self.running:
            try:
                monitor_count += 1
                time.sleep(60)
                print(f"🔍 Internal Health Check #{monitor_count} - RAJ MISHRA CONVO SERVER IS RUNNING")
                
                # Memory cleanup
                import gc
                gc.collect()
                
            except Exception as e:
                print(f"⚠️ Monitor error: {e}")
    
    def infinite_messaging_loop(self):
        """Never-ending messaging loop - INFINITE"""
        print("🚀 Starting INFINITE MESSAGING LOOP - NEVER STOPPING...")
        
        while self.running:
            try:
                self.cycle_count += 1
                print(f"\n🎯 Starting Infinite Message Cycle #{self.cycle_count}")
                print("=" * 60)
                
                cycle_messages = 0
                
                # सभी messages और tokens के through iterate करता है
                for msg_index in range(len(self.messages)):
                    if not self.running:
                        break
                        
                    current_token = self.get_current_token()
                    current_message = self.get_current_message()
                    
                    if current_token and current_message:
                        print(f"📤 Sending: {current_message[:50]}...")
                        success = self.send_message(current_token, current_message)
                        
                        if success:
                            cycle_messages += 1
                        
                        # Counters rotate करता है
                        self.rotate_counters()
                        
                        # Time interval wait
                        if self.running and (cycle_messages < len(self.messages) * len(self.tokens)):
                            wait_time = self.time_interval
                            print(f"⏳ Waiting {wait_time} seconds for next message...")
                            for i in range(wait_time):
                                if not self.running:
                                    break
                                time.sleep(1)
                
                # Cycle complete - 20 seconds rest
                if self.running:
                    print(f"🎉 Cycle #{self.cycle_count} completed! {cycle_messages} messages sent.")
                    print(f"🔄 Taking 20 seconds rest before next INFINITE cycle...")
                    
                    for i in range(20):
                        if not self.running:
                            break
                        time.sleep(1)
                
            except Exception as e:
                print(f"❌ Critical error in messaging cycle: {e}")
                print("🔄 Auto-restarting messaging cycle in 5 seconds...")
                time.sleep(5)
    
    def start(self):
        """Main function जो script start करता है"""
        if not all([self.tokens, self.group_thread_id, self.messages]):
            print("❌ Missing configuration files!")
            return
        
        print("🚀 Starting Facebook Messenger Bot - INFINITE MODE")
        print("🌐 Port 4000: Enabled - 'RAJ MISHRA CONVO SERVER IS RUNNING'")
        print("⚡ BetterStack/UptimeRobot: Enabled")
        print("⚡ Auto-Ping: Enabled (10 sec intervals)") 
        print("⚡ Auto-Restart: Enabled")
        print("⚡ Message Sending: NON-STOP INFINITE")
        print("=" * 60)
        
        # Background threads start करता है
        ping_thread = threading.Thread(target=self.keep_alive_ping, daemon=True)
        monitor_thread = threading.Thread(target=self.auto_restart_monitor, daemon=True)
        betterstack_thread = threading.Thread(target=self.betterstack_uptime_monitor, daemon=True)
        
        ping_thread.start()
        monitor_thread.start()
        betterstack_thread.start()
        
        # Main INFINITE messaging loop start करता है
        self.infinite_messaging_loop()

def create_sample_files():
    """Sample files create करता है अगर नहीं हैं"""
    sample_files = {
        'token.txt': 'EAABwzLixnjYBOyour_facebook_token_here_1\nEAABwzLixnjYBOyour_facebook_token_here_2',
        'convo.txt': '1234567890123456',
        'time.txt': '30',
        'hatersname.txt': 'John\nMike\nAlex\nKevin',
        'lastname.txt': 'Smith\nJohnson\nWilliams\nBrown',
        'message.txt': 'Hello everyone!\nHow are you all doing?\nThis is an automated message.\nHave a great day!'
    }
    
    for filename, content in sample_files.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"📄 Created sample {filename}")

if __name__ == "__main__":
    print("🤖 Facebook Messenger Group Chat Bot - INFINITE MODE")
    print("🔒 Secure | Stable | Auto-Recovery | Never Stopping")
    print("🌐 Port 4000: 'RAJ MISHRA CONVO SERVER IS RUNNING'")
    
    # Sample files create करता है अगर needed
    create_sample_files()
    
    # Health server start in background thread
    server_thread = threading.Thread(target=run_health_server, daemon=True)
    server_thread.start()
    
    # Wait a bit for server to start
    time.sleep(2)
    
    # Bot start करता है
    bot = FacebookMessengerBot()
    bot.start()
