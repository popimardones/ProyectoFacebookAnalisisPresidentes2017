import requests
import json

#LO SIGUIENTE CREA UNA LISTA DEL CONTENIDO QUE TIENE UN ARCHIVO TXT
#CAMBIAR POR CADA CANDIDATO
fileRead = open('AlejandroNavarroPostIds2.txt')

#crear una lista de todos los post ids, pero todos los items tienen \n al final
presidente_txtList= fileRead.readlines()

#saca el \n de todos los item de la lista
presidenteSacarSlashNList= [i.replace('\n','') for i in presidente_txtList]

#saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
#CAMBIAR POR CADA CANDIDATO
presidenteSoloPostId_List = [i.replace('10152723078_','') for i in presidenteSacarSlashNList]

#sacar el ultimo termino de la lista porque el archivo tiene una linea en blanco
presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]

#se puede ver esto al imprimir cada lista
print(presidente_txtList)
print(presidenteSacarSlashNList)
print(presidenteSoloPostId_List)

fileRead.close()
#####################################

graph_api_version = 'v2.9'
#cambiar token cada hora aprox
access_token = 'EAACEdEose0cBAOo0g2aGHWHQ6ILZBjZC5T4rtdX4SukdjiwDtEXRzc2wxW6rfZB12RjKznNGlxRbkBMyd26ZCyIxnxthZAAySfjtpdQrZC6Dd4Gj9V36vuA12KoqZCmAo33eSFq5Y3ZCNt1R54M0ZCsdRJdeOZA0Q2aAOtYWZCKSh1E9J4riQDx9MmMeyeBLBuFoZCkZD'

#user id (id del candidato; CAMBIAR POR CADA CANDIDATO)
user_id = '10152723078'

for id in presidenteSoloPostId_List:
    
    # the graph API
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
            comments.append(comment)
        
        # check if there are more comments
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])
            print('Encontrados {} comments'.format(len(data['data'])))
        else:
            break
#guardar los comentarios en un archivo json para cada publicación del candidato
with open('AlejandroNavarroCommentsOfPost' + id + '.json', 'w', encoding='utf-8') as outfile:
    json.dump(comments, outfile, indent=4, ensure_ascii=False)
