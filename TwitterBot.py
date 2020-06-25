import sys
import os
import tweepy
import random
import time
import module

#Stores last seen Tweet IDs in order to not repeat
FILE_NAME = 'last_seen_id.txt'

#Twitter API Information
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

print('*Initializing* - Waiting for Rate Limit Approval')
api = tweepy.API(auth, wait_on_rate_limit=True)

running = True
wait_time = 0
print('*Initializing*')
mentions = api.mentions_timeline()
api.update_profile('AaronP', description='AaronP Developer account for recreational use of the Twitter API\n\nDm me with feature ideas!\n\nFeatures: http://pastebin.com/3UKNJevP\nStatus: Online')
print('Initiated Successfully')
while running:
    mentions = api.mentions_timeline()

    last_seen_id = module.retrieve_last_seen_id(FILE_NAME)

    found = False

    for mention in mentions:
        if mention.id <= last_seen_id:
            found = True
            break

    if not found:
        found = True

    else:
        found = False

    for mention in reversed(mentions):
        lastID = mention.id
        if mention.id <= last_seen_id:
            found = True
            continue
        if found:
            print(str(mention.id) + ' - ' + mention.text)

            if 'via @AaronPDev' in mention.text:
                print('Own tweet found')
                continue

            if '#test' in mention.text.lower():
                print('Found #Test')
            try:  # If there is an image present in the tweet this run the functions they requested
                length = len(mention.extended_entities['media'])
                for i in range(0, length):
                    if '#circles' in mention.text.lower():
                        print('Circles Found!')
                        try:
                            module.circles(api, mention, mention.extended_entities['media'][i]['media_url'])
                        except:
                            continue

                    if '#compress' in mention.text.lower():
                        print('compress Found!')
                        try:
                            module.compress(api, mention, mention.extended_entities['media'][i]['media_url'], 2)
                        except:
                            continue

                    if '#compressx2' in mention.text.lower():
                        print('compressx2 Found!')
                        try:
                            module.compress(api, mention, mention.extended_entities['media'][i]['media_url'], 4)
                        except:
                            continue

            except:
                if '#maze' in mention.text.lower():
                    module.maze(api, mention)
                    print('maze Found')

                if '#kill' in mention.text.lower():
                    running = False
                    print('Killing Bot')
                    _hash_ = random.randrange(0, 99999999, 1)
                    api.update_status("Stopping!  via @AaronPDev " + str(_hash_), in_reply_to_mentions_id=mention.id)
                    api.update_profile('AaronP', description='AaronP Developer account for recreational use of the Twitter API\n\nDm me with feature ideas!\n\nFeatures: http://pastebin.com/3UKNJevP\nStatus: Offline')
                    break

    module.store_last_seen_id(lastID, FILE_NAME)


    if not running:
        break

    if wait_time % 3 == 0:
        print('sleeping...')

    wait_time += 1
    time.sleep(6)
