"""СКРИПТ ОТСЕИВАЕТ НУЖНУЮ ИНФОРМАЦИЮ ИЗ ДИРЕКТОРИИ json/, И ЗАПИСЫВАЕТ В followers.json"""



import glob
import json
from pprint import pprint

files = glob.glob("json/*.json")
followers = {}

for file in files:
    with open(file, 'r') as file:
        data = json.load(file)
        for follower in data['data']['user']['edge_followed_by']['edges']:
            followers_data = follower['node']
            followers[followers_data['id']] = {
                'id' : followers_data['id'],
                'username' : followers_data['username'],
                'followed_by_viewer' : followers_data['followed_by_viewer'],
                'full_name' : followers_data['full_name'],
            }
followers = list(followers.values())

with open('followers.json', 'w') as file:
    json.dump(followers, file)
print('SUCCESS')




