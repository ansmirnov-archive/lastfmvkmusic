from django.shortcuts import render_to_response, redirect
import json
import urllib
from common import secret
import users
import models
import time
import re

def process_code(request):
	code, lastfm_user = [request.GET.get(x, '') for x in 'code', 'lastfm_user']
	f = urllib.urlopen('https://oauth.vkontakte.ru/access_token?client_id=%s&client_secret=%s&code=%s' % (secret.VK_CLIENT_ID, secret.VK_CLIENT_SECRET, code))
	resp = f.read()
	res = json.loads(resp)
	access_token = res['access_token']
	user_id = res['user_id']
	users.add_user(vk_id=user_id, access_token=access_token, lastfm_user=lastfm_user)
	return redirect('http://lastfm.initab.ru/vkstatus/?alert=vkstatus_add_ok')

def send_last(request):
	lastfm_user = request.GET.get('lastfm_user', '')
	at_url = request.GET.get('access_token', '')
	access_token = re.search('access_token\=([^&]*)\&', at_url).groups()[0]
	vk_id = int(re.search('user_id\=(.*)$', at_url).groups()[0])
#	a = access_token
	try:
		user = models.VKUser.objects.get(vk_id=vk_id)
	except:
		user = models.VKUser(vk_id=vk_id)
	user.pattern = request.GET.get('pattern', '')
	user.broadcast_audio = bool(request.GET.get('broadcast_audio', ''))
	user.lastfm_user = lastfm_user
	user.access_token = access_token
	user.save()
	return redirect('http://lastfm.initab.ru/vkstatus/?alert=vkstatus_add_ok')
#	return render_to_response('send_last.html', {'lastfm_user': lastfm_user, 'a': a})

def iteration(request):
	for user in models.VKUser.objects.all():
		lastfm_user, access_token, last_status = user.lastfm_user, user.access_token, user.last_status
		try:
			xml = urllib.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='+lastfm_user+'&limit=1&api_key=8fe4d75f5e7f7853f926237db752641e').read()
		except:
			continue
		r = re.search("""<track nowplaying="true">""", xml)
		try:
			r.groups(0)
			r = re.search("""<artist mbid="[^"]*">([^<]*)</artist>""", xml)
			artist = r.groups(0)[0]
			r = re.search("""<name>([^<]*)</name>""", xml)
			track = r.groups(0)[0]
			status = artist + ' - ' + track
			a = ''
			url = 'https://api.vk.com/method/status.set?text=Now playing: '+status+'&access_token='+str(access_token)
			if status != last_status:
				if int(time.time()) - user.status_update_time > 0 or last_status == '':
					a += urllib.urlopen(url).read()
					#write_param(user_id, 'last_status', status)
					user.last_status = status;
					user.status_update_time = int(time.time())
					user.save()
		except:
			if last_status != '':
				if int(time.time()) - user.status_update_time > 0:
					url = 'https://api.vk.com/method/status.set?text=&access_token='+str(access_token)
					urllib.urlopen(url).read()
					#write_param(user_id, 'last_status', '')
					user.last_status = '';
					user.status_update_time = int(time.time())
					user.save()
	return render_to_response('test.html');
	
