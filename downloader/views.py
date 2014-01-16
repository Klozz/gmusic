# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from downloader.models import *
from django.core import serializers
import re
import json
import requests

def home(request):
    recent_searchs = Search.objects.all().order_by('-date')[:5]
    return render_to_response('home.html', locals(), RequestContext(request))

def ultimas_canciones_json(request):
    recent_searchs = Search.objects.all().order_by('-date')[:5]
    searchs = serializers.serialize('json', recent_searchs, sort_keys=True, indent=4)
    return HttpResponse(searchs, content_type="application/json",mimetype='application/json')

def buscar_cancion_json(request):
    search = request.GET.get('name_song')
    contenido1 = requests.get("http://www.goear.com/search/"+search)
    contenido2 = requests.get("http://www.goear.com/search/"+search+"/1")
    contenido = contenido1.text + contenido2.text

    names = re.findall(r'<span class="song">([-.\s\w]+)</span>',contenido)
    artists = re.findall(r'<span class="group">([-.\s\w]+)</span>', contenido)
    ids = re.findall(r'href="http://www.goear.com/listen/([\w\d]+)/',contenido)
    qualitys = re.findall(r'<li class="kbps radius_3">([\d]+)<abbr title="Kilobit por segundo">kbps</abbr></li>', contenido)
    lengs = re.findall(r'<li class="length radius_3">([-:\d]+)</li>', contenido)
 
    songs = (None if not len(names) else [])

    for i, name in enumerate(names):
        try:
            songs.append({'name': name, 'artist': artists[i], 'id': ids[i], 'quality': qualitys[i], 'len': lengs[i]})
        except:
            pass

    model_search = Search(name=search.replace('-',' '),result=(False if not songs else True))
    model_search.save()

    return HttpResponse(json.dumps(songs, sort_keys=True, indent=4), content_type="application/json",mimetype='application/json')