import requests, json, os, time, sys

API_URL = 'https://rechat.twitch.tv/rechat-messages'
BE_NICE = 0

"""
v5 Twitch API got rid of getting a channel by name. This method provides
a workaround by parsing the get_channel response using the login name and channel_id
"""
def get_channel(name):
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': credentials['client-id'], 'info': 'where are the rechat docs'}
    url = 'https://api.twitch.tv/kraken/users?login=' + name
    response = requests.get(url, headers=headers) 
    data = json.loads(response.text)
    if int(data['_total']) > 1:
        print("Multiple results")
    else:
        channel_id = data['users'][0]['_id']
        url = 'https://api.twitch.tv/kraken/channels/' + channel_id
        return requests.get(url, headers=headers)

def make_request(start_time, video_id):
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    return API_URL + '?client_id=' + str(credentials['client-id']) + '&start=' + str(start_time) + '&video_id=v' + str(video_id)

"""
downloads the chat log of video with passed video_id
writes to file named <video-id>-chatlog.txt
"""
def download_chat_log(video_id):
    # parse credentials
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    # request chat log, guranteed 400 error because start != 0 for given video_id
    response = requests.get(make_request(0, video_id)).json()

    # parse response for true start and end time
    details = response['errors'][0]['detail'].split(' ')
    start, end = int(details[4]), int(details[6])
    current = start

    # open write to file
    fw = open('../logs/' + str(video_id) + '-chatlog.txt', 'w')

    messages = []
    
    begin_time = time.time()
    while current <= end:
        response = requests.get(make_request(current, video_id)).json()

        # check for duplicate messages
        for msg in response['data']:
            if msg['id'] not in messages:
                messages.append(msg['id'])
                fw.write(json.dumps(msg, indent=4, sort_keys=True))

        current += 30
        progress = round(float((current - start) / (end - start)) * 100, 2)
        sys.stdout.write("Progess: " + str(progress) + "%\r")
        sys.stdout.flush()
        time.sleep(BE_NICE)

    fw.close()
    print("Downloaded chat replay for v" + str(video_id) + " in " + str(int(time.time() - begin_time)) + "s")
    











