from django.core.management.base import NoArgsCommand
from vkstatus import models
import json
import urllib
import re
import time

class Command(NoArgsCommand):
    help = 'test'
    def handle_noargs(self, **options):
#	access_token = 'e582cb91ef1b1841ef1b184114ef31e3e2eef1bef1a1c49bfac7bbb4d037dfcf4ce206b'
	url = 'https://api.vk.com/method/audio.search?q=Eurythmics - Sweet Dreams (Are Made Of This)&sort=2&count=1&access_token='+str(access_token)
	r = json.loads(urllib.urlopen(url).read())['response'][1]
#	print r
	url = 'https://api.vk.com/method/status.set?audio='+str(r['owner_id'])+'_'+str(r['aid'])+'&access_token='+str(access_token)
#	url = 'https://api.vk.com/method/status.get?access_token='+str(access_token)
	print json.loads(urllib.urlopen(url).read())
