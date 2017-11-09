#cada vez que descargues los postIds de un presidente, hay que ir cambiando el user_id
import requests

graph_api_version = 'v2.9'

'''lo tuve que ir refreshing cada hora y no tuve problemas con facebook'''
access_token = 'EAACEdEose0cBAMjJPnKZCFtmnwhERcPbbsCL2uvMjsRDwDJ1a06bwZC1KAdzFZC5w4e2s6u66NzVfADm6iCj4xuB9MwNunWLsGM5y7AzP1kJ8YkrkhEpwp5yDiOKkUOmiZCSqD7oKuV5nhRoL8BHzVrvwyv8OFFA1vlEblVsG0oRSNtmZCCJ9wChH5tWlyKeIpT2EHrwsKgZDZD'

# presidentes' Facebook user id
user_id = '1481491872064849' #en este caso es de alejandro guillier

# the graph API endpoint for ids on presidente's post
url = 'https://graph.facebook.com/{}/{}/posts'.format(graph_api_version, user_id)

#hacer una lista de los post_ids
postIds = []
r = requests.get(url, params={'access_token': access_token})
while True:
    data = r.json()

    # catch errors returned by the Graph API
    if 'error' in data:
        raise Exception(data['error']['id'])

    # append the text of each id into the postIds list
    for id in data['data']:
        # remove line breaks in each id
        text = id['id'].replace('\n', ' ')
        postIds.append(text)

    print('got {} postIds'.format(len(data['data'])))

    # check if there are more postIds
    if 'paging' in data and 'next' in data['paging']:
        r = requests.get(data['paging']['next'])
    else:
        break

# guardar los postIds a un archivo llamado NombreDePresidentePostIds.txt
with open('PresiPostIds.txt', 'w', encoding='utf-8') as f:
    for id in postIds:
        f.write(id + '\n')