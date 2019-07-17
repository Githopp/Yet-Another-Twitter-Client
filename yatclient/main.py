

import tweepy
import pandas as pd
import numpy as np

from tweet_analyzer import TweetAnalyzer
#from tweet_plotter import TweetPlotter
from twitter_client import TwitterClient

pd.options.display.max_columns = 100


CONSUMER_KEY = "25aKeI8DFf2ew44LSslNwoRBn"
CONSUMER_SECRET = "kkbU4dBNpA9k0Rcu11VMHAt9uv9LjnOohsnaL3xW4itthwOtf1"
ACCESS_TOKEN =  "555424234-wwFaAuK0kYO0V8WTlx71kTwyuQRIRq0QmI8hoRoX"
ACCESS_TOKEN_SECRET = "lLKEDEXnrunCqe9lQ56BkE0XtLdTv9BMKRTmtxGMbtXJl"
################################################
################################################
################################################


#twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ["spdde"])
#twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei"])

#tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-05-01", end_date = "2019-05-26", retweets = False)

#analyzer_load1 = TweetAnalyzer(tweets)
#print(analyzer_load1.get_dataframe())



#tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-05-01", end_date = "2019-05-26", retweets = False, max_id = analyzer_load1.get_dataframe().id.iloc[-1])

#analyzer_load2 = TweetAnalyzer(tweets)
#print(analyzer_load2.get_dataframe())







#Parties = ["afd"]
#Parties = ["die_Gruenen","afd","diepartei"]
#Parties = ["cducsubt", "cdu","csu"]
#Parties = ["spdde"]
Parties = ["die_Gruenen"]
#Parties = ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei","cdu","csu"]

#Parties = ["spdde"]
twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, Parties)

import datetime

EuropawahlDate = datetime.date(2019, 5, 27)
ThreeWeeksBeforeDate = EuropawahlDate - datetime.timedelta(weeks=3)
today = datetime.date.today()



tweets = twitter_client.get_user_timeline_tweets(start_date = str(ThreeWeeksBeforeDate), end_date = str(EuropawahlDate))

analyzer = TweetAnalyzer(tweets)

analyzer.tweet_filter_retweets(min_number_of_retweets = 25)
#print(analyzer.bagofwords(on="hashtags",extended_view=False))
analyzer.plot_bar(type="hashtags", xvalues = True, title = "Top 20 most common Green party hashtags", count = 20)

analyzer.plot_bar(type="la_ct", xvalues = True, count = 20)
#analyzer.plot_trend(type="retweets", show_each_account = True, yticksize = 100)
#analyzer.plot_bar(type="la_ct", count = 20)
analyzer.plot_bar(type="wct", edgecolor="black", alpha=1.0, stopOWN = ["mehr"])
#analyzer.plot_hist(type = "likes", bins=5,facecolor = "green",alpha = 1)
#analyzer.plot_trend(type = "count", show_each_account = True, yticksize=10)

analyzer.plot_bar_sum(type="retweets", xvalues = True)




# tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-06-28", end_date = "2019-07-02", retweets = False)
#
# analyzer_load2 = TweetAnalyzer(tweets)
# print(analyzer_load2.get_dataframe())
#
# analyzer_load3 = TweetAnalyzer(df = analyzer_load1.get_dataframe())
# analyzer_load3.merge_dataframe(analyzer_load2.get_dataframe())
# print(analyzer_load3.get_dataframe())



#analyzer_load.write_to_csv("test.csv", encoding = "utf-8")



# analyzer = TweetAnalyzer()
# analyzer.read_from_csv("test.csv")
# print(analyzer.get_dataframe())

#print(analyzer.get_dataframe().dtypes)

#print(analyzer.get_dataframe())
#print(list(analyzer.df.columns.values))
#print(analyzer.df["hashtags"])

#print(analyzer.bagofwords(on = "tweets", extended_view = False))


#analyzer.plot_trend(type="retweets", show_each_account = True, yticksize = 100)
#analyzer.plot_bar(type="la_ct", count = 20)
#analyzer.plot_bar(type="wct", edgecolor="black", alpha=1.0, stopOWN = ["mehr"])
#analyzer.plot_hist(type = "likes", bins=5,facecolor = "green",alpha = 1)
#analyzer.plot_trend(type = "count", show_each_account = True, yticksize=10)
