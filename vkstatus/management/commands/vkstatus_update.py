from django.core.management.base import NoArgsCommand
from vkstatus import models
import json
import urllib
import re
import time

class Command(NoArgsCommand):
    help = 'Update statuses for all users'
    def handle_noargs(self, **options):
	for user in models.VKUser.objects.all():
#	for user in models.VKUser.objects.filter(lastfm_user='rc_d'):
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
			if user.saved_status == 'NoneST':
				url = 'https://api.vk.com/method/status.get?access_token='+str(access_token)
				user.saved_status = json.loads(urllib.urlopen(url).read())['response']['text']
				user.save()
			a = ''
			status = user.pattern
			if status == '':
				status = 'Now playing: %artist% - %track%'
			_status = status.encode('utf8')
			_status = _status.replace('%artist%', artist)
			_status = _status.replace('%track%', track)
			_status = _status.replace('&amp;', '%26')
			status = _status.decode('utf8')
#			url = 'https://api.vk.com/method/status.set?text=Now playing: '+status+' (vk.cc/QZeWu)&access_token='+str(access_token)
			
			if status != last_status:
				if int(time.time()) - user.status_update_time > 0 or last_status == '':
					if user.broadcast_audio == True:
						q = artist + ' - ' + track
						url = 'https://api.vk.com/method/audio.search?q='+q+'&sort=2&count=1&access_token='+str(access_token)
						r = json.loads(urllib.urlopen(url).read())['response'][1]
						url = 'https://api.vk.com/method/status.set?audio='+str(r['owner_id'])+'_'+str(r['aid'])+'&access_token='+str(access_token)
						a = urllib.urlopen(url).read()
					else:
						url = 'https://api.vk.com/method/status.set?text='+_status+'&access_token='+str(access_token)
						a = urllib.urlopen(url).read()
						#write_param(user_id, 'last_status', status)
					print a
					user.last_status = status;
					user.status_update_time = int(time.time())
					user.save()
		except (KeyError, AttributeError):
			if last_status != '':
				if int(time.time()) - user.status_update_time > 300:
#				if int(time.time()) - user.status_update_time > 0:
					saved_status = user.saved_status.encode('utf8')
					if saved_status == 'NoneST': saved_status = ''
					saved_status = saved_status.replace('&amp;', '%26')
					url = 'https://api.vk.com/method/status.set?text=%s&access_token=%s' % (saved_status, str(access_token))
					user.saved_status = 'NoneST'
					urllib.urlopen(url).read()
					#write_param(user_id, 'last_status', '')
					user.last_status = '';
					user.status_update_time = int(time.time())
					user.save()
	#return render_to_response('test.html');
	
