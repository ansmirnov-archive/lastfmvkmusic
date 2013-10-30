import models

def add_user(vk_id, access_token, lastfm_user):
	try:
		user = models.VKUser.objects.get(lastfm_user=lastfm_user)
		user.access_token, user.lastfm_user, user.vk_id = access_token, lastfm_user, vk_id
	except:
		user = models.VKUser(vk_id=vk_id, access_token=access_token, lastfm_user=lastfm_user)
	user.saved_status = 'NoneST'
	user.save()
	return user
