import operator
from collections import Counter

from django.shortcuts import render
from django.http import HttpResponse
from helpers.oauth_changed import OAuth2API
from instagram.client import InstagramAPI

CLIENT_ID = "a9fd754cac6145939423517998c97c96"
CLIENT_SECRET = "91058f21a2cb480a87e71ac80c9d75c3"
REDIRECT_URI = "http://cryptic-reaches-8531.herokuapp.com/home"

def index(request):
	return render(request, 'best_time_teller/index.html', {})

def home(request):
	code = str(request.GET.get('code'))
	oauth = OAuth2API(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
	access_token, user_info = oauth.exchange_code_for_access_token(code)
	# access_token, user_info = ('1327109423.a9fd754.8a4991734ff942ac9af1065eca26b96e', {'bio': u'', 'full_name': 'Bharadwaj Srigiriraju', 'id': '1327109423', 'website': u'', 'profile_picture': 'http://images.ak.instagram.com/profiles/anonymousUser.jpg', 'username': 'bharadwajsrigiriraju'})
	request.session['access_token'] = access_token
	api = InstagramAPI(access_token=access_token)
	user_id = user_info['id']
	follower_list, page_no = api.user_followed_by(user_id)
	recent_timings = []
	feed = api.user_media_feed()
	media_feed = feed[0]
	for media in media_feed:
		recent_timings.append(media.created_time)
	hours = []
	days = {}
	for datetime_obj in recent_timings:
		hours.append(datetime_obj.hour)
		day = datetime_obj.today().weekday()

		if day not in days:
			days[day] = 0
		else:
			days[day] += 1
	hours_count = dict(Counter(hours))
	sorted_hours = sorted(hours_count.items(), key=operator.itemgetter(1))
	days_count = dict(Counter(days))
	sorted_days = sorted(days_count.items(), key=operator.itemgetter(1))
	res = []
	day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	day_number = int(sorted_days[len(sorted_days)-1][0])
	for i in xrange(3):
		astring = "The " + str(i+1) + " best time for you is: " + str(int(sorted_hours[len(sorted_hours)-i-1][0])-1) + ":30"
		res.append(astring)
	res.append("<br> The best day for you is: " + str(day_name[day_number]))
	
	# for follower in follower_list:
	# 	follower_id = follower.id
	# 	recent_timings.append(api.user_recent_media(follower_id))
	
	return HttpResponse('<br>'.join(res))
