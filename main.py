import requests
import json
import time
import os
import threading
from colorama import init, Fore, Style

init(autoreset=True)

class MaskedTool:
    def __init__(self):
        self._masked_webhook = ""
        self._masked_message = ""
        self._masked_username = "github.com/masked1337"
        self._masked_avatar = "https://cdn.discordapp.com/attachments/1431947784088588348/1438937303807688869/d1ownload.jfif?ex=6918b24b&is=691760cb&hm=bf1d2590ca94367b36bb387a634339d01cb9ca6555f83b2f999cd393cd4c70d2"
        self._masked_delay = 1
        self._masked_count = 0
        self._masked_sent = 0
        self._masked_active = False
        self._masked_threads = 1
        
    def _masked_send_message(self, thread_id=0):
        payload = {
            "content": self._masked_message,
            "username": self._masked_username,
            "avatar_url": self._masked_avatar
        }
        
        try:
            response = requests.post(
                self._masked_webhook,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                self._masked_sent += 1
                return True
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                time.sleep(retry_after / 1000)
                return self._masked_send_message(thread_id)
            else:
                print(f"{Fore.RED}❌ Error {response.status_code} in thread {thread_id}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Connection error in thread {thread_id}: {e}")
            return False
    
    def _masked_thread_worker(self, thread_id):
        while self._masked_active and (self._masked_count == 0 or self._masked_sent < self._masked_count):
            if self._masked_send_message(thread_id):
                print(f"{Fore.GREEN}✅ Message {self._masked_sent} sent (Thread {thread_id})")
            
            if self._masked_delay > 0:
                time.sleep(self._masked_delay)
    
    def masked_start(self):
        if not self._masked_webhook or not self._masked_message:
            return f"{Fore.RED}❌ Please configure webhook URL and message first"
        
        self._masked_active = True
        self._masked_sent = 0
        
        print(f"{Fore.CYAN}🚀 Starting spam with {self._masked_threads} threads...")
        print(f"{Fore.YELLOW}⏹️ Press Ctrl+C to stop")
        
        threads = []
        try:
            for i in range(self._masked_threads):
                thread = threading.Thread(target=self._masked_thread_worker, args=(i+1,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            
            while self._masked_active and (self._masked_count == 0 or self._masked_sent < self._masked_count):
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self._masked_active = False
        
        for thread in threads:
            thread.join(timeout=1)
            
        return f"✅ Completed! Sent {self._masked_sent} messages"
    
    def masked_stop(self):
        self._masked_active = False
    
    def masked_set_webhook(self, url):
        self._masked_webhook = url
    
    def masked_set_message(self, message):
        self._masked_message = message
    
    def masked_set_delay(self, delay):
        self._masked_delay = delay
    
    def masked_set_count(self, count):
        self._masked_count = count
    
    def masked_set_threads(self, threads):
        self._masked_threads = max(1, min(threads, 10))
    
    def masked_get_info(self):
        return {
            'sent': self._masked_sent,
            'webhook': self._masked_webhook[:50] + "..." if len(self._masked_webhook) > 50 else self._masked_webhook,
            'message': self._masked_message[:30] + "..." if len(self._masked_message) > 30 else self._masked_message,
            'username': self._masked_username,
            'delay': self._masked_delay,
            'target_count': self._masked_count,
            'threads': self._masked_threads
        }

def masked_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    masked = MaskedTool()
    
    while True:
        masked_clear()
        print(f"{Fore.CYAN}🤖 Discord Webhook Spammer")
        print(f"{Fore.WHITE}1. Set Webhook URL")
        print(f"{Fore.WHITE}2. Set Message")
        print(f"{Fore.WHITE}3. Configure Settings")
        print(f"{Fore.WHITE}4. Start Spamming")
        print(f"{Fore.WHITE}5. View Statistics")
        print(f"{Fore.RED}0. Exit")
        print()
        
        choice = input(f"{Fore.YELLOW}Select option: ")
        
        if choice == '1':
            masked_clear()
            print(f"{Fore.CYAN}🔗 Set Webhook URL")
            info = masked.masked_get_info()
            if info['webhook']:
                print(f"{Fore.WHITE}Current: {info['webhook']}")
            
            webhook = input("Webhook URL: ").strip()
            if webhook:
                masked.masked_set_webhook(webhook)
                print(f"{Fore.GREEN}✅ Webhook URL set!")
            input("Press Enter to continue...")
            
        elif choice == '2':
            masked_clear()
            print(f"{Fore.CYAN}💬 Set Message")
            info = masked.masked_get_info()
            if info['message']:
                print(f"{Fore.WHITE}Current: {info['message']}")
            
            message = input("Message: ").strip()
            if message:
                masked.masked_set_message(message)
                print(f"{Fore.GREEN}✅ Message set!")
            input("Press Enter to continue...")
            
        elif choice == '3':
            masked_clear()
            print(f"{Fore.CYAN}⚙️ Configure Settings")
            info = masked.masked_get_info()
            
            print(f"{Fore.WHITE}Current delay: {info['delay']}s")
            print(f"{Fore.WHITE}Current target count: {info['target_count']} (0 = unlimited)")
            print(f"{Fore.WHITE}Current threads: {info['threads']}")
            
            try:
                delay = input("Delay between messages (seconds): ").strip()
                if delay:
                    masked.masked_set_delay(float(delay))
                
                count = input("Total messages to send (0 for unlimited): ").strip()
                if count:
                    masked.masked_set_count(int(count))
                
                threads = input("Number of threads (1-10): ").strip()
                if threads:
                    masked.masked_set_threads(int(threads))
                
                print(f"{Fore.GREEN}✅ Settings updated!")
            except ValueError:
                print(f"{Fore.RED}❌ Invalid input!")
            input("Press Enter to continue...")
            
        elif choice == '4':
            masked_clear()
            info = masked.masked_get_info()
            if not masked._masked_webhook or not masked._masked_message:
                print(f"{Fore.RED}❌ Please set webhook URL and message first!")
                input("Press Enter to continue...")
                continue
            
            print(f"{Fore.CYAN}🚀 Starting Webhook Spam")
            print(f"{Fore.WHITE}🔗 Webhook: {info['webhook']}")
            print(f"{Fore.WHITE}💬 Message: {info['message']}")
            print(f"{Fore.WHITE}👤 Username: {info['username']}")
            print(f"{Fore.WHITE}⏱️ Delay: {info['delay']}s")
            print(f"{Fore.WHITE}🎯 Target: {info['target_count'] if info['target_count'] > 0 else 'Unlimited'}")
            print(f"{Fore.WHITE}🧵 Threads: {info['threads']}")
            print(f"{Fore.YELLOW}⏹️ Press Ctrl+C to stop")
            
            input("\nPress Enter to start...")
            result = masked.masked_start()
            
            masked_clear()
            print(f"{Fore.CYAN}{result}")
            input("Press Enter to continue...")
            
        elif choice == '5':
            masked_clear()
            print(f"{Fore.CYAN}📊 Statistics")
            info = masked.masked_get_info()
            print(f"{Fore.WHITE}📨 Messages sent: {info['sent']}")
            print(f"{Fore.WHITE}🔗 Webhook: {info['webhook']}")
            print(f"{Fore.WHITE}💬 Message: {info['message']}")
            print(f"{Fore.WHITE}👤 Username: {info['username']}")
            print(f"{Fore.WHITE}⏱️ Delay: {info['delay']}s")
            print(f"{Fore.WHITE}🎯 Target count: {info['target_count']}")
            print(f"{Fore.WHITE}🧵 Threads: {info['threads']}")
            input("Press Enter to continue...")
            
        elif choice == '0':
            masked_clear()
            print(f"{Fore.CYAN}👋 Goodbye!")
            break
            
        else:
            print(f"{Fore.RED}❌ Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}⏹️ Program stopped by user")