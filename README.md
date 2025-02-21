# Render Monitoring Tool

The Render Monitoring Tool is a simple application designed to monitor the uptime of web applications hosted on the Render platform. It checks the application's status at regular intervals and sends alerts via Telegram when the application becomes inactive.

## Features

- Monitors a specified Render-hosted application.

- Sends Telegram notifications when the application fails to respond.

- Configurable inactivity threshold for alerts.

## Requirements

- Python 3.7+

- requests library

- python-dotenv library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/codefromlani/render-monitoring-tool.git

2. Navigate to the project directory:

    cd render-monitoring-tool

3. Install Dependencies

    ```bash
    pip install requests python-dotenv

4. Environment Variables
- Create a .env file in the project directory with the following variables:

    ```bash
    RENDER_APP_URL=<your_render_app_url>
    TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
    TELEGRAM_CHAT_ID=<your_telegram_chat_id>
    INACTIVITY_THRESHOLD_MINUTES=15  # Optional, default is 15 minutes

4. Run the Application

    ```bash
    python main.py

## Usage

The application will continuously monitor the specified Render app URL and send a Telegram notification if it becomes inactive for longer than the defined threshold.