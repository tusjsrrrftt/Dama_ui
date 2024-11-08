import os
import sys
import logging
import datetime
import json
import time
import threading

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ui.chat_interface import ChatGPTStyleInterface
from config.api_keys import GROQ_API_KEY
from utils.logging_config import setup_logging
from utils.network_check import check_internet_connection

LAST_CLEAN_FILE = os.path.join(project_root, 'last_clean.json')

def load_last_clean_date():
    if os.path.exists(LAST_CLEAN_FILE):
        with open(LAST_CLEAN_FILE, 'r') as f:
            data = json.load(f)
            return datetime.datetime.fromisoformat(data['last_clean'])
    return None

def save_last_clean_date():
    with open(LAST_CLEAN_FILE, 'w') as f:
        json.dump({'last_clean': datetime.datetime.now().isoformat()}, f)

def clean_data():
    logger = logging.getLogger(__name__)
    last_clean = load_last_clean_date()
    now = datetime.datetime.now()

    if last_clean is None or (now - last_clean).days >= 7:
        logger.info("Running weekly data cleanup...")
        # Add your cleaning logic here
        # For example:
        # - Delete old log files
        # - Clear temporary data
        # - Remove cached files older than a certain date
        logger.info("Weekly data cleanup completed.")
        save_last_clean_date()
    else:
        logger.info("Skipping cleanup, last cleanup was less than a week ago.")

def check_and_clean():
    while True:
        clean_data()
        time.sleep(86400)  # Sleep for 24 hours

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # Start the cleaning check thread
    cleaning_thread = threading.Thread(target=check_and_clean)
    cleaning_thread.daemon = True
    cleaning_thread.start()

    # Check for internet connection
    if not check_internet_connection():
        logger.error("No internet connection available. Exiting the program.")
        print("Error: No internet connection available. Please check your connection and try again.")
        sys.exit(1)

    try:
        app = ChatGPTStyleInterface(GROQ_API_KEY)
        app.mainloop()
    except Exception as e:
        logger.error(f"An error occurred while starting the application: {str(e)}")
        print(f"An error occurred: {str(e)}")
    finally:
        sys.exit(1)

if __name__ == "__main__":
    main()