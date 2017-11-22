import requests
import json

graph_api_version = 'v2.9'
access_token = 'EAACEdEose0cBAOo0g2aGHWHQ6ILZBjZC5T4rtdX4SukdjiwDtEXRzc2wxW6rfZB12RjKznNGlxRbkBMyd26ZCyIxnxthZAAySfjtpdQrZC6Dd4Gj9V36vuA12KoqZCmAo33eSFq5Y3ZCNt1R54M0ZCsdRJdeOZA0Q2aAOtYWZCKSh1E9J4riQDx9MmMeyeBLBuFoZCkZD'

#user id
user_id = '553775568008058'

# the id of LHL's response post at https://www.facebook.com/leehsienloong/posts/1505690826160285
post_id = '1717696668282603'

# the graph API endpoint for comments on LHL's post
url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, post_id)

comments = []

r = requests.get(url, params={'access_token': access_token})
while True:
    data = r.json()

    # catch errors returned by the Graph API
    if 'error' in data:
        raise Exception(data['error']['message'])

    # append the text of each comment into the comments list
    for comment in data['data']:
        comments.append(comment)

    # check if there are more comments
    if 'paging' in data and 'next' in data['paging']:
        r = requests.get(data['paging']['next'])
        print('Encontrados {} posts'.format(len(data['data'])))
    else:
        break

with open('try5.json', 'w', encoding='utf-8') as outfile:
    json.dump(comments, outfile, indent=4, ensure_ascii=False)
