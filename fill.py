import json
import subprocess
from pprint import pprint
import time


with open('followers.json', 'r') as file:
    followers = json.load(file)


command_template = """curl 'https://www.instagram.com/{username}/?__a=1' \
-H 'authority: www.instagram.com' \
-H 'pragma: no-cache' \
-H 'cache-control: no-cache' \
-H 'accept: */*' \
-H 'x-ig-www-claim: hmac.AR3zxZkkL8C1lgGiaAMKGQT5saUfdtl4-e7JfNL69kntSSJy' \
-H 'x-requested-with: XMLHttpRequest' \
-H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
-H 'x-ig-app-id: 936619743392459' \
-H 'sec-fetch-site: same-origin' \
-H 'sec-fetch-mode: cors' \
-H 'sec-fetch-dest: empty' \
-H 'referer: https://www.instagram.com/inga.mirinova.75/' \
-H 'accept-language: ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7' \
-H 'cookie: ig_did=FE3C7978-F70A-41DE-96A1-FF6E4808CA1D; mid=X3buYAALAAHnX2d2iZ-YayCT4g1x; shbid=17738; shbts=1601629798.9769788; rur=FRC; csrftoken=TOHyypzGHsfquNZXHXgXVGqS7wPzsAay; ds_user_id=37512042523; sessionid=37512042523%3AGcfCi30Ills60P%3A22; urlgen="{{\"46.0.96.63\": 34533}}:1kOhTz:uTOpxvRVZNvPTB5HV0IthJzd3aY"' \
--compressed > temp.json"""

index = 1
full_data_followers = []
for follower in followers:
    subprocess.run(command_template.format(username=follower['username']), shell=True, capture_output=True)

    with open('temp.json', 'r') as file:
        data = json.load(file)


    
    follower['follows'] = data['graphql']['user']['edge_follow']['count']
    follower['count_posts'] = data['graphql']['user']['edge_owner_to_timeline_media']['count']
    
    full_data_followers.append(follower)
    
    print(f'Iteration {index}/{len(followers)}')
    

    index += 1

with open('full_data_folowers.csv', 'w') as file:
    file.write(f"Full Name, Username, Follows, Count Posts\n")
    for follower in full_data_followers:
        file.write(f"{follower['full_name']},{follower['username']},{follower['follows']},{follower['count_posts']}\n") 


