from django.db import models
import time

class VKUser (models.Model):
	vk_id = models.IntegerField(db_index=True, default=-int(time.time()))
	access_token = models.CharField(max_length=100, default='')
	lastfm_user = models.CharField(max_length=100, default='')
	last_status = models.CharField(max_length=400, default='')
	status_update_time = models.IntegerField(default=0)
	saved_status = models.CharField(max_length=400, default='')
	pattern = models.CharField(max_length=200, default='')
	broadcast_audio = models.BooleanField(default=False)
	def __unicode__(self):
		return "id%d, %s" % (self.vk_id, self.lastfm_user)
