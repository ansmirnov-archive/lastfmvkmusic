from django.shortcuts import render_to_response

import os

def site_page(request):
	p = request.path.split('?')[0].split('/')
	default_lang = 'rus';
	lang = request.COOKIES.get('lang', default_lang);
	if len(p) == 1 or request.path == '/':
#	    lang = 'rus'
	    page = 'about'
	elif len(p) == 2 or len(p) == 3 and p[2] == '':
#	    lang = 'rus'
	    page = p[1]
	else:
#	    lang = p[1]
	    page = p[2]
	template_name = lang + '/' + page +'.html'
	alerts = {}
	if request.GET.get('alert', '') == 'vkstatus_add_ok':
		alerts['vkstatus'] = 'success'
	return render_to_response(template_name, {
	    'lang': lang,
	    'page': page,
	    'alerts': alerts,
	})
