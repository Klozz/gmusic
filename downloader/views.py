# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from downloader.models import *
from httplib2 import Http
from django.contrib import messages
import re
import json
from django.core import serializers


http = Http()

def home(request):
	recent_searchs = Search.objects.all().order_by('-date')[:5]
	return render_to_response('home.html', locals(), RequestContext(request))

def ultimas_cancones_json(request):
	recent_searchs = Search.objects.all().order_by('-date')[:5]
	searchs = serializers.serialize('json', recent_searchs, sort_keys=True, indent=4)
	return HttpResponse(searchs, content_type="application/json",mimetype='application/json')

def buscar_cancion_json(request):
	search = request.GET.get('name_song')
	contenido1 = http.request("http://www.goear.com/search/"+search)[1]
	contenido2 = http.request("http://www.goear.com/search/"+search)[1]
	contenido = contenido1 + contenido2
	songs = []
	names = re.findall(r'<span class="song">([-.\s\w]+)</span>',contenido)
	artist = re.findall(r'<span class="group">([-.\s\w]+)</span>', contenido)
	ids = re.findall(r'href="http://www.goear.com/listen/([\w\d]+)/',contenido)
	qualitys = re.findall(r'<li class="kbps radius_3">([\d]+)<abbr title="Kilobit por segundo">kbps</abbr></li>', contenido)
	lengs = re.findall(r'<li class="length radius_3">([-:\d]+)</li>', contenido)

	if len(names) == 0:
		songs = None
		result = False
	else:
		for i in range(0,len(names)):
			try: 
				songs.append({'name':names[i], 'artist':artist[i],'id':ids[i],'quality': qualitys[i], 'len': lengs[i]})
			except:
				pass

		result = True

	model_search = Search(name=search.replace('-',' '),result=result)
	model_search.save()

	return HttpResponse(json.dumps(songs, sort_keys=True, indent=4), content_type="application/json",mimetype='application/json')