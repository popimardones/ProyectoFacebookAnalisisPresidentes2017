#how to read a file
#en este caso abrir el archivo creado donde estan todos los postIds de Alejandro Navarro
fileRead = open('AlejandroNavarroPostIds2.txt')
#crear una lista de todos los post ids, pero todos los items tienen \n al final
presidente_txtList= fileRead.readlines()
#saca el \n de todos los item de la lista
presidenteSacarSlashNList= [i.replace('\n','') for i in presidente_txtList]
#saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
presidenteSoloPostId_List = [i.replace('10152723078_','') for i in presidenteSacarSlashNList]
#sacar el ultimo termino de la lista porque por alguna razon es un item empty
presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]
#se puede ver esto al imprimir cada lista
print(presidente_txtList)
print(presidenteSacarSlashNList)
print(presidenteSoloPostId_List)

fileRead.close()

'''como todos los post de alejandro guillier tienen el user_id identico, solo hacer una iteracion
de los post id, por lo tanto eliminar 1481491872064849_ de la lista para solo tener
una lista de los postId
'''

import requests

graph_api_version = 'v2.9'
#cambiar el token cada hora
access_token = 'EAACEdEose0cBAFTZBbkB83u5nEp05VWFyotwmeHlPAs4HykZCRIeQlrlNKUtoesmuIQViJJ0Smjb7Fkw3xXTZCfRlFygkP0iL7kkq8PfaZBaKz37MUYc0hj0f8QH2oHML3vF1tpvI3w5jiyZAqAoziMSwbosmCwEjHSS6ey2SKoGmoMT4ycLUBCkhFdR4cdF64jpJt6NKZAQZDZD'

# presidentes' Facebook user id
user_id = '10152723078' #en este caso es de alejandro navarro

for id in presidenteSoloPostId_List:
    # the graph API endpoint for comments on presi's post
    url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, id)

    comments = []

    r = requests.get(url, params={'access_token': access_token})
    while True:
        data = r.json()

        # catch errors returned by the Graph API
        if 'error' in data:
            raise Exception(data['error']['message'])

        # append the text of each comment into the comments list
        for comment in data['data']:
            # remove line breaks in each comment
            text = comment['message'].replace('\n', ' ')
            comments.append(text)

        print('got {} comments'.format(len(data['data'])))

        # check if there are more comments
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])
        else:
            break

    # guardar los comentarios de cada post en un archivo
    # nombrar el archivo el nombre del presidente + el id + .txt
    with open('AlejandroNavarroCommentsOfPost' + id + '.txt', 'w', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment + '\n')


