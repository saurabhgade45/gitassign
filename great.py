import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'QZqskJ9NgTQBkKDIFBdOYyLhm'
		consumer_secret = 'qHGke4c0IwnaX1Foqs6dcDCtvCTsn3SA79buxvP7vJRQQdKjM5'
		access_token = '1175279623862538241-BjK4Xw217UMJSSeKi7l0TZN0wLzp6f'
		access_token_secret = 'dQbQOwCMQUBxS8RLQGRkRfdUMqcSr7tHyR0oLEYl3UXLP'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
									

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	# calling function to get tweets
	query = input("topic you want to search")
	count = int(input("number of tweets you want to analyse"))
	tweets = api.get_tweets(query, count)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	positivet = int(100*len(ptweets)/len(tweets))
	#print("ptweet",positivet)
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	negativet = int(100*len(ntweets)/len(tweets))
	#print("ptweet",negativet)
	# percentage of neutral tweets
	nuetralt = int(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))
	#print("neutral",nuetralt)
	print("Neutral tweets percentage: {} % \
		".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

	# printing first 5 positive tweets
	#print("\n\nPositive tweets:")
	#for tweet in ptweets[:10]:
		#print(tweet['text'])

	# printing first 5 negative tweets
	#print("\n\nNegative tweets:")
	#for tweet in ntweets[:10]:
		#print(tweet['text'])

	sizes = [positivet,negativet,nuetralt]
	mylabels = ['positive','negative','neutral']
	mycolors = ['green','red','yellow']
	plt.pie(sizes, labels=mylabels, colors=mycolors, startangle=90)
	plt.show()
    

if __name__ == "__main__":
	# calling main function
	main()
