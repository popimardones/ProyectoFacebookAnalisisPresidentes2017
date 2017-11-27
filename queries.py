from pymongo import MongoClient
import sys
import io
from language_detector import LanguageDetector
from corpus import CorpusHelper, CorpusModel
import json
import facebook
ch = CorpusHelper(language='spanish')
ch.load()
cm = CorpusModel(corpus=ch)
params = cm.fit()
print('Our model has an AUC of {}'.format(cm.x_validation(params)))
candidatos = ['AlejandroGuillier', 'SebastianPiñera', 'AlejandroNavarro', 'CarolinaGoic', 'BeatrizSanchez', 'JoseAntonioKast', 'EduardoArtes', 'MarcoEnriquez-Ominami']
client = MongoClient('localhost', 27017)
candidatoId = ['1481491872064849', '553775568008058', '10152723078', '377671865775887', '137510593443379', '881095048648989', '321406001578434', '386634201382499'] 
#candidatoId ordenado segun la lista "candidatos"
posicionId = 0
aprobaciones= []
aprobacionesNumero= []
candidatosPubliNoVacias= []
candidatosPubliVacias= []
meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre']
for candidato in candidatos:
	publiVacias=0
	publiNoVacias=0
	totalComentarios = 0
	totalPositivos = 0
	IdCandidatoActual = candidatoId[posicionId]
	database = client[candidato+"JSONcomments"]
	for mes in meses:
		sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'backslashreplace')
		positivosEnMes = 0
		comentariosEnMes = 0
		fileRead = open(candidato+'_postIds_'+mes+'.txt', 'r')
		presidente_txtList = fileRead.readlines()
		# saca el \n de todos los item de la lista
		presidenteSacarSlashNList = [i.replace('\n', '') for i in presidente_txtList]
		# saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
		presidenteSoloPostId_List = [i.replace(IdCandidatoActual+'_', '') for i in presidenteSacarSlashNList]
		# sacar el ultimo termino de la lista porque por alguna razon es un item empty
		presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]
		comments = []
		for x in range(0, len(presidenteSoloPostId_List)):
			collection = database[candidato+"CommentsOfPost"+presidenteSoloPostId_List[x]]
			query = {}
			projection = {}
			projection["message"] = 1
			cursor = collection.find(query, projection = projection)
			try:
			    for doc in cursor:
			        comments.append(doc["message"])
			finally:
			    cursor.close()
		if len(comments) > 0:
			publiNoVacias = publiNoVacias + 1
			lista = cm.predict(comments, params)
		else:
			publiVacias = publiVacias + 1
		#print(comments)
		comentariosEnMes = len(comments)
		print(candidato)
		print(mes)
		print('Cantidad de publicaciones: {}'.format(len(presidenteSoloPostId_List)))
		print('Comentarios en publicacion: {}'.format(comentariosEnMes))
		promedioMes= (comentariosEnMes/len(presidenteSoloPostId_List))
		print('Promedio de comentarios por publicacion: {}'.format(promedioMes))
		for index in range(0, len(lista)):
			positivosEnMes += lista[index]
		porcentajePositivoEnMes = ((positivosEnMes / comentariosEnMes) * 100)
		print("{0:0.2f}% aprobación".format(porcentajePositivoEnMes))
		print("\n")
		totalComentarios += comentariosEnMes
		totalPositivos += positivosEnMes
	posicionId +=1
	print(candidato)
	print('Total comentarios: ')
	print(totalComentarios)
	porcentajePositivoTotal = ((totalPositivos/ totalComentarios)*100)
	print("{0:0.2f}% aprobación".format(porcentajePositivoTotal))
	print("\n")
	print("cambio de candidato")
	#Listas con aprobaciones, publicaciones no vacias y vacias
	aprobaciones.append(porcentajePositivoTotal)
	aprobacionesNumero.append(totalPositivos)
	candidatosPubliNoVacias.append(publiNoVacias)
	candidatosPubliVacias.append(publiVacias)
print()
print("PORCENTAJE DE POSITIVIDAD DE LOS COMENTARIOS DE FACEBOOK DE LAS PUBLICACIONES DE LOS CANDIDATOS:\n")
for i in range(len(candidatos)):
    print(candidatos[i]+ ': {0:0.2f}% - {1} Comentarios positivos'.format(aprobaciones[i], aprobacionesNumero[i]))
    #print('  Publicaciones con comentarios: {}'.format(candidatosPubliNoVacias[i]))
    #print('  Publicaciones vacias: {}'.format(candidatosPubliVacias[i]))
    print()
