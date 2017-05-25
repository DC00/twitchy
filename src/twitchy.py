from lib import *
import json

if __name__ == '__main__':
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    download_chat_log(116722636)
