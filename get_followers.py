import subprocess
import time
import urllib.parse
import json
from pprint import pprint

base_url = 'https://www.instagram.com/graphql/query/?'

command_template ="""curl '{url}' \
-H 'authority: www.instagram.com' \
-H 'pragma: no-cache' \
-H 'cache-control: no-cache' \
-H 'accept: */*' \
-H 'x-ig-www-claim: hmac.AR3zxZkkL8C1lgGiaAMKGQT5saUfdtl4-e7JfNL69kntSY6q' \
-H 'x-requested-with: XMLHttpRequest' \
-H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
-H 'x-csrftoken: TOHyypzGHsfquNZXHXgXVGqS7wPzsAay' \
-H 'x-ig-app-id: 936619743392459' \
-H 'sec-fetch-site: same-origin' \
-H 'sec-fetch-mode: cors' \
-H 'sec-fetch-dest: empty' \
-H 'referer: https://www.instagram.com/mairou_politics/followers/' \
-H 'accept-language: ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7' \
-H 'cookie: ig_did=FE3C7978-F70A-41DE-96A1-FF6E4808CA1D; mid=X3buYAALAAHnX2d2iZ-YayCT4g1x; shbid=17738; shbts=1601629798.9769788; rur=FRC; csrftoken=TOHyypzGHsfquNZXHXgXVGqS7wPzsAay; ds_user_id=37512042523; sessionid=37512042523%3AGcfCi30Ills60P%3A22; urlgen="{{\"46.0.96.63\": 34533}}:1kOKk3:zTAUVN7s33GbvOHQc4jkBxCUwz0"' \
--compressed > json/instagram_response_{index}.json"""


index = 1
after = None
followers_in_progress = 0
while True:
    after_value = f', "after":"{after}"' if after else ''
    variables = f'{{"id":"37512042523","include_reel":true,"fetch_mutual":false,"first":13{after_value}}}' 
    get_params = {
        'query_hash' : 'c76146de99bb02f6415203be841dd25a', 
        'variables' : variables
    }
    
    url_with_params = base_url + urllib.parse.urlencode(get_params)
    result = subprocess.run(command_template.format(url=url_with_params, index=index), shell=True, capture_output=True)
    if result.returncode != 0:
        exit('OOps(')
    
    with open(f'json/instagram_response_{index}.json', 'r') as file:
        data = json.load(file
                )
    if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
        break
   
    after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
    all_followers = data['data']['user']['edge_followed_by']['count']
    count_parsed_followers = len(data['data']['user']['edge_followed_by']['edges'])
    followers_in_progress += count_parsed_followers
    print(f'Parsed: {followers_in_progress}/{all_followers}')
    

    time.sleep(5 if index % 10 != 0 else 20)
    index += 1

print('SUCCESS')

