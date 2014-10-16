from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import RequestContext, loader

def index(request):
	return render(request, 'best_time_teller/index.html', {})

def home(request):
	return HttpResponse(str(request.GET))
