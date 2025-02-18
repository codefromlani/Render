import os
import time
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RenderMonitor:
    def __init__(self, app_url, inactivity_threshold_minutes=15):
        """
        Initialize the monitor with app URL and inactivity threshold.
        
        Args:
            app_url (str): The URL of your Render-hosted application
            inactivity_threshold_minutes (int): Minutes of inactivity before notification
        """
        self.app_url = app_url.rstrip('/')
        self.inactivity_threshold = timedelta(minutes=inactivity_threshold_minutes)
        self.last_active_time = datetime.now()
        
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not all([self.telegram_bot_token, self.telegram_chat_id]):
            raise ValueError("Missing required environment variables")

    def check_app_status(self):
        
        try:
            response = requests.get(self.app_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Error checking app status: {str(e)}")
            return False

    def send_telegram_notification(self, message):
        
        telegram_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        
        try:
            response = requests.post(telegram_url, json={
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            })
            response.raise_for_status()
            logger.info("Notification sent successfully")
        except requests.RequestException as e:
            logger.error(f"Failed to send notification: {str(e)}")

    def monitor(self):
        logger.info(f"Starting monitoring for {self.app_url}")
        
        while True:
            current_time = datetime.now()
            
            if self.check_app_status():
                logger.info("App is active")  
            else:
                message = (
                    f"⚠️ <b>App Inactivity Alert</b>\n\n"
                    f"🌐 App: {self.app_url}\n"
                    f"⏰ Failed to respond within 5 seconds\n"
                    f"📅 Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                self.send_telegram_notification(message)
            time.sleep(60)  

def main():
    
    app_url = os.getenv('RENDER_APP_URL')
    inactivity_threshold = int(os.getenv('INACTIVITY_THRESHOLD_MINUTES', '15'))
    
    if not app_url:
        raise ValueError("RENDER_APP_URL environment variable is required")
    
    monitor = RenderMonitor(app_url, inactivity_threshold)
    monitor.monitor()

if __name__ == "__main__":
    main()