#!/usr/bin/python3
# encoding=utf-8
import tweepy
import vk
from vkappauth import VKAppAuth
import time

# Параметры приложения TWITTER
TWITTER_CONSUMER_KEY='L8u8DhjY8OZ2hqHfRnNPkwklQE'
TWITTER_CONSUMER_SECRET='jMr2lNiRoFKcywtAXFKx8NkrKEepn6yLfs67r5U484m1mmkz6UE'

# Токен авторизованного приложения TWITTER
TWITTER_OAUTH_TOKEN={'oauth_token': '2684990353-aixOSVqT1UFCDpkHfOwrFNybszrnMlKgY4pwFCNE', 'oauth_token_secret': 'ZT4YjqnkNn4rHHfllxXal8ayAfFp7ZZw2qhyyfPz97LWRE'}

# Идентификатор приложения Вконтакте
# Механизм доступа к сене описан https://vk.com/dev/auth_mobile
VK_APP_ID='4944920'
VK_LOGIN='+79237794486'
VK_PASSWORD='t1MlGxthxWmB'

# Авторизация приложения по PIN-коду
def twitter_get_authorization_tokens():
	oauth_client=tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
	                                   TWITTER_CONSUMER_SECRET)
	try:
		url_with_token=oauth_client.get_authorization_url()
	except tweepy.TweepError:
		print ('Ошибка получения url для авторизации.')
		return None
	print ('Пожалуйста перейдите по ссылке: \n'+url_with_token+'\nдля авторизации приложения и введите полученный PIN-код.')
	print ('PIN: ')
	verifier = input()
	try:
		oauth_client.get_access_token(verifier)
		access_tokens={}
		access_tokens['oauth_token']=oauth_client.access_token
		access_tokens['oauth_token_secret']=oauth_client.access_token_secret
		return access_tokens
	except tweepy.TweepError:
		print ('Ошибка получения токена доступа.')
		return None

# Загружаем все твиты
def get_all_tweetts(oauth_token,user):
	tweets=[]
	auth=tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
	auth.set_access_token(TWITTER_OAUTH_TOKEN['oauth_token'], TWITTER_OAUTH_TOKEN['oauth_token_secret'])
	api=tweepy.API(auth)
	last_tweets=api.user_timeline(screen_name=user,count=5)
	tweets.extend(last_tweets)
	old_id=tweets[-1].id-1
	new_tweets=tweets
	while len(new_tweets)>0:
		new_tweets=api.user_timeline(screen_name=user,count=5,max_id=old_id)
		tweets.extend(new_tweets)
		old_id=tweets[-1].id-1
	for tweet in tweets:
		print (tweet.text)
	return tweets

# Публикуем новый твит с разбивкой на несколько при привышении объема сообщения
def publish_tweet(tweet,oauth_token):
	tweets=[]
	words=tweet.split(' ')
	chars=0
	max_message_len=140
	message=''
	delimeter=''
	auth=tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
	auth.set_access_token(TWITTER_OAUTH_TOKEN['oauth_token'], TWITTER_OAUTH_TOKEN['oauth_token_secret'])
	api=tweepy.API(auth)
	for word in words:
		word_len=len(word)+1
		chars=chars+word_len
		if chars>max_message_len:
			chars=word_len
			tweets.append(message)
			message=word+' '
		else:
			message=message+delimeter+word
			delimeter=' '
	tweets.append(message)
	for tweet in tweets:
		api.update_status(status=tweet)
		time.sleep(5)
	return None

#def vk_get_authorization_tokens():
#	vkaa=VKAppAuth()
#	scope = ['wall', 'offline']
#	token=vkaa.auth(VK_LOGIN, VK_PASSWORD, VK_APP_ID, scope)
#	return token

#def get_all_vk_wall_records(login,password):
#	records=[]
#	return records

# Получение доступа к стене Vkontakte (Чтение/Запись)
#print (vk_get_authorization_tokens())

# Получение доступа к Twitter (чтение/запись)
#print (get_authorization_tokens())

# Получаем все твиты авторизованного пользователя
#print (get_all_tweetts(TWITTER_OAUTH_TOKEN,'chanton14'))

# Публикуем твит с разбивкой на отдельные сообщения
#print (publish_tweet('Солдатик-шоферюга возит командира части.\
#Дважды в неделю он отвозит его к любовнице.\
#Однажды, видя хорошее настроение шефа, он набрался борзости и спросил:\
#- Товарищ полковник, разрешить задать вам вопрос?\
#- Валяй!\
#- У вас такая жена чудесная, а вы к любовнице ездите. Почему?\
#Полковник нахмурился и ничего не ответил...\
#Солдатик думает: "Ну, всё! Мне хана: переведут на ассенизаторскую машину...".\
#Утром приходит авторота на завтрак. Всем, как обычно, овёс. А ему, персонально, жареной картошечки с котлеткой, а вместо киселя с бромом - кофе! Так же в обед и на ужин...\
#Через два месяца боец взмолился:\
#- Товарищ полковник, я эту картошку жареную уже видеть не могу, в глотку не лезет!\
#- Вот видишь, сынок, тебе за два месяца надоело, а я с женой уже двадцать пять лет живу. Понял теперь?!..',TWITTER_OAUTH_TOKEN))

#print (publish_tweet('Сейчас запостим длинный анекдот',TWITTER_OAUTH_TOKEN))
