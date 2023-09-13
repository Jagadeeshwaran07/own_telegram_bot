import http.client
import json
import re

# Replace with your Telegram bot token and custom URL shortening service API token
TELEGRAM_BOT_TOKEN = '6622977839:AAG4uiM66M7NsRp9WfYq8UDes4gfkQXOSpQ'
BITLY_API_TOKEN = 'ee7491b5da17b2c43e5b8cf2f5c1137c'

# Keep track of the latest update ID to avoid processing the same update multiple times
latest_update_id = None

# Function to send a message via the Telegram bot
def send_message(chat_id, text):
    conn = http.client.HTTPSConnection("api.telegram.org")
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text
    })
    headers = {'Content-Type': 'application/json'}

    conn.request("POST", f"/bot{TELEGRAM_BOT_TOKEN}/sendMessage", payload, headers)
    res = conn.getresponse()
    data = res.read()

# Function to shorten URLs using a custom URL shortening service
def shorten_url(url):
    conn = http.client.HTTPSConnection("urlbae.com")
    headers = {
        "Authorization": f"Bearer {CUSTOM_SHORTENER_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = json.dumps({
        "url": url
    })

    conn.request("POST", "/api/url/add", data, headers)
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        return json.loads(data)["shorturl"]
    else:
        return None

# Process incoming messages
def process_message(update):
    global latest_update_id  # Make sure to use the latest_update_id from the outer scope
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    update_id = update["update_id"]

    # Check if the update has already been processed
    if update_id <= latest_update_id:
        return

    # Update the latest update_id to the current update
    latest_update_id = update_id

    if text.startswith('/start'):
        response_text = "Hi! Send me a URL, and I will shorten it for you."
    else:
        # Use regular expression to find URLs in the message
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        if urls:
            for url in urls:
                shortened_url = shorten_url(url)
                if shortened_url:
                    response_text = f"Shortened URL: {shortened_url}"
                    send_message(chat_id, response_text)
                else:
                    response_text = "Invalid URL"
                    send_message(chat_id, response_text)
        else:
            response_text = "No URLs found in the message"
            send_message(chat_id, response_text)

# Main function
def main():
    while True:
        try:
            conn = http.client.HTTPSConnection("api.telegram.org")
            conn.request("GET", f"/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={latest_update_id + 1}&timeout=60")
            res = conn.getresponse()
            data = res.read()
            updates = json.loads(data)["result"]

            if updates:
                for update in updates:
                    process_message(update)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()



# import http.client
# import json

# # Replace with your Telegram bot token an

# TELEGRAM_BOT_TOKEN = '6622977839:AAG4uiM66M7NsRp9WfYq8UDes4gfkQXOSpQ'
# BITLY_API_TOKEN = 'ee7491b5da17b2c43e5b8cf2f5c1137c'

# # Function to send a message via the Telegram bot
# def send_message(chat_id, text):
#     conn = http.client.HTTPSConnection("api.telegram.org")
#     payload = json.dumps({
#         "chat_id": chat_id,
#         "text": text
#     })
#     headers = {'Content-Type': 'application/json'}

#     conn.request("POST", f"/bot{TELEGRAM_BOT_TOKEN}/sendMessage", payload, headers)
#     res = conn.getresponse()
#     data = res.read()

# # Function to shorten URLs using Bitly
# def shorten_url(url):
#     conn = http.client.HTTPSConnection("urlbae.com")
#     headers = {
#         "Authorization": f"Bearer {BITLY_API_TOKEN}",
#         "Content-Type": "application/json",
#     }
#     data = json.dumps({
#         "url": url
#     })

#     conn.request("POST", "/api/url/add", data, headers)
#     res = conn.getresponse()
#     data = res.read()

#     if res.status == 200:
#         return json.loads(data)["shorturl"]
#     else:
#         return None

# # Process incoming messages
# def process_message(update):
#     chat_id = update["message"]["chat"]["id"]
#     text = update["message"]["text"]

#     if text.startswith('/start'):
#         response_text = "Hi puks! Send me a URL, and I will shorten it for you."
#     elif text.startswith(("http://", "https://")):
#         # url_to_shorten = text
#         shortened_url = shorten_url(text)
#         if shortened_url:
#             response_text = f"Shortened URL: {shortened_url}"
            
#         else:
#             response_text = "Invalid puks"
#     else:
#         response_text = "Enna ma idhu"

#     send_message(chat_id, response_text)

# # Main function
# def main():
#     update_id = 0

#     while True:
#         try:
#             conn = http.client.HTTPSConnection("api.telegram.org")
#             conn.request("GET", f"/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={update_id + 1}&timeout=60")
#             res = conn.getresponse()
#             data = res.read()
#             updates = json.loads(data)["result"]

#             if updates:
#                 for update in updates:
#                     process_message(update)
#                     update_id = update["update_id"]
#         except Exception as e:
#             print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()
