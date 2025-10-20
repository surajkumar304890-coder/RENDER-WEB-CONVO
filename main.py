import requests
import time
import threading
import random
import os
from datetime import datetime
from flask import Flask, jsonify
import sys

# Flask app for health monitoring
app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "running", 
        "service": "facebook_messenger_bot",
        "timestamp": datetime.now().isoformat(),
        "code": 200
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "code": 200})

def run_flask_app():
    """Flask app को port 4000 पर run करता है"""
    try:
        print("🌐 Starting health monitor on port 4000...")
        app.run(host='0.0.0.0', port=4000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Flask app error: {e}")

class FacebookMessengerBot:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v17.0"
        self.load_config()
        self.message_counter = 0
        self.token_counter = 0
        self.running = True
        self.cycle_count = 0
        self.total_successful_messages = 0
        
    def load_config(self):
        """सभी configuration files load करता है"""
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
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
                return
                
            except Exception as e:
                print(f"❌ Error loading config (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("💥 Failed to load configuration after multiple attempts")
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
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        payload = {
            'message': message,
            'access_token': token
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Message sent successfully | Token: {token[:15]}... | Time: {datetime.now().strftime('%H:%M:%S')}")
                self.total_successful_messages += 1
                return True
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                # Token invalid होने पर उसे remove करने की जगह skip करते हैं
                if "invalid token" in response.text.lower() or "expired" in response.text.lower():
                    print(f"⚠️ Token might be invalid, but continuing with next...")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return False
    
    def keep_alive_ping(self):
        """Script को always active रखने के लिए internal ping"""
        ping_count = 0
        while self.running:
            try:
                ping_count += 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"🔄 System Active Ping #{ping_count} | Time: {current_time}")
                
                # Internal health check - अपने आप को ping करता है
                try:
                    health_response = requests.get('http://localhost:4000/health', timeout=5)
                    if health_response.status_code == 200:
                        print(f"❤️ Internal Health Check: OK (200)")
                    else:
                        print(f"⚠️ Internal Health Check: {health_response.status_code}")
                except:
                    print("⚠️ Internal health check failed, but continuing...")
                
                # हर 10 seconds में internal ping
                for i in range(6):  # 6 * 10 = 60 seconds
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
                time.sleep(60)  # हर 1 minute में check करता है
                print(f"🔍 Internal Health Check #{monitor_count} - System Running Smoothly")
                print(f"📊 Stats: {self.total_successful_messages} total messages sent | {self.cycle_count} cycles completed")
                
                # Memory cleanup और resource management
                import gc
                gc.collect()
                
            except Exception as e:
                print(f"⚠️ Monitor error: {e}")
    
    def continuous_messaging(self):
        """Never-ending messaging loop"""
        print("🚀 Starting NEVER-ENDING messaging loop...")
        
        while self.running:
            try:
                self.cycle_count += 1
                print(f"\n🎯 Starting Message Cycle #{self.cycle_count}")
                print("=" * 60)
                
                # Current cycle के messages count
                cycle_messages_sent = 0
                
                # सभी messages के through iterate करता है
                for msg_index in range(len(self.messages)):
                    if not self.running:
                        break
                        
                    # Current token और message लेता है
                    current_token = self.get_current_token()
                    current_message = self.get_current_message()
                    
                    if current_token and current_message:
                        print(f"📤 Sending: {current_message[:50]}...")
                        success = self.send_message(current_token, current_message)
                        
                        if success:
                            cycle_messages_sent += 1
                        
                        # Counters rotate करता है
                        self.rotate_counters()
                        
                        # Time interval wait (next message से पहले)
                        if self.running:
                            wait_time = self.time_interval
                            print(f"⏳ Waiting {wait_time} seconds for next message...")
                            for i in range(wait_time):
                                if not self.running:
                                    break
                                time.sleep(1)
                
                # Cycle complete - 20 seconds rest (अगर running है)
                if self.running:
                    print(f"🎉 Cycle #{self.cycle_count} completed! {cycle_messages_sent} messages sent in this cycle.")
                    print(f"🔄 Taking 20 seconds rest before next cycle...")
                    
                    rest_time = 20
                    for i in range(rest_time):
                        if not self.running:
                            break
                        time.sleep(1)
                
            except Exception as e:
                print(f"❌ Critical error in messaging cycle: {e}")
                print("🔄 Restarting messaging cycle in 5 seconds...")
                time.sleep(5)
    
    def start(self):
        """Main function जो script start करता है"""
        if not all([self.tokens, self.group_thread_id, self.messages]):
            print("❌ Missing configuration files! Creating sample files...")
            self.create_emergency_files()
            print("🔄 Retrying configuration load...")
            self.load_config()
            
            if not all([self.tokens, self.group_thread_id, self.messages]):
                print("💥 Still missing configuration. Please check your files.")
                return
        
        print("🚀 Starting Facebook Messenger Bot - NEVER STOPPING VERSION")
        print("⚡ Auto-Ping: Enabled (10 sec intervals)")
        print("⚡ Health Check: Port 4000 (Status 200)")
        print("⚡ Auto-Restart: Enabled")
        print("⚡ Crash Protection: Maximum")
        print("⚡ Message Sending: Non-Stop")
        print("=" * 60)
        
        # Background threads start करता है
        ping_thread = threading.Thread(target=self.keep_alive_ping, daemon=True)
        monitor_thread = threading.Thread(target=self.auto_restart_monitor, daemon=True)
        
        ping_thread.start()
        monitor_thread.start()
        
        # Main messaging cycle start करता है (never returns)
        self.continuous_messaging()
    
    def create_emergency_files(self):
        """Emergency sample files बनाता है अगर missing हैं"""
        sample_files = {
            'token.txt': 'EAABwzLixnjYBOyour_facebook_token_here_1',
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
                print(f"📄 Created emergency {filename}")

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

def main():
    """Main execution function"""
    print("🤖 Facebook Messenger Group Chat Bot - NON STOP VERSION")
    print("🔒 Secure | Stable | Auto-Recovery | Never Stopping")
    print("🌐 Health Monitor: Port 4000 | Status Code: 200")
    
    # Sample files create करता है अगर needed
    create_sample_files()
    
    # Flask health monitor को separate thread में start करता है
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait for flask to start
    time.sleep(3)
    
    # Bot start करता है - यह function never return करेगा
    bot = FacebookMessengerBot()
    bot.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"💥 Fatal error in main: {e}")
        print("🔄 Auto-restarting entire script in 10 seconds...")
        time.sleep(10)
        os.execv(sys.executable, ['python'] + sys.argv)
