
#import twitter_credentials - comment style because in __init__
import re

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters  # used in plot_trend
from sklearn.feature_extraction.text import CountVectorizer


class TweetAnalyzer:
    """
    Description
    -----------
    Functionality for analyzing and categorizing content from tweets.
    It is based on the TwitterClient Class, which returns the "raw" data.
    """
    def __init__(self, tweets = None, df = None):
        """
        Description
        -----------
        This class can be initialized via the data fetched by TwitterClient().get_user_timeline_tweets(): The raw tweet data.
        If no dataframe is provided, it will automaticly create a dataframe, including metadata (see function: tweets_to_dataframe)

        IMPORTANT:
        If you create a TweetAnalyzer object by passing a custom dataframe:
        Make sure it has the same structure (column names/data types) as the one created by the class function: tweets_to_dataframe!

        If you don't provide any tweets and no Dataframe: FUNCTIONS will obviously not work!
        --> You can load csv, excel, json as a dataframe and work with it (see functions write_to_csv, write_to_excel, write_to_json)

        Parameters
        ----------
        tweets:             type = <class 'list'>
                            description =  A list created by the TwitterClient Class which is using tweepy package to obtain the raw tweets via the twitter API
                            default = None

        df:                 type = <class 'pandas.core.frame.DataFrame'>
                            description = Dataframe, which includes several meta data on every tweet
                            default = None

        Returns
        -------
        <class 'tweet_analyzer.TweetAnalyzer'>

            --> By calling, it instantiates a TweetAnalyzer Object

        Example(s)
        ----------
        The following examples instantiates a TweetAnalyzer with the account of Donald Trump.

        1.
            >>>> consumer_key = "Example_xyz1"
            >>>> consumer_secret = "Example_xyz2"
            >>>> access_token = "Example_xyz3"
            >>>> access_token_secret = "Example_xyz4"
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TwitterClient(tweets)
        """
        if tweets == None:
            self.tweets = tweets
            self.df = df

        else:
            self.tweets = tweets
            self.df = df if df is not None else self.tweets_to_dataframe(self.tweets)

######DATAFRAME##################################################################################################################################
    def tweets_to_dataframe(self,tweets):
        """
        Description
        -----------
        This function creates a dataframe of the TwitterClient().get_user_timeline_tweets() returned tweets list:
        By obtaining serveral informations of the tweets object, stored in separate columns, we get:
        * The tweet text
        * The Account ("author of the tweet")
        * The date (when the tweet was tweeted)
        * The number of likes for each tweet
        * The number of retweets for each tweet
        * The source of the tweet (from which device it was posted)
        * The hashtags
        * The linked accounts
        * The urls
        * The ID
        * The Tweet Type

        Parameters
        ----------
        tweets:             type = <class 'list'>
                            description = A list created by the TwitterClient Class which is using tweepy package to obtain the raw tweets via the twitter API

        Returns
        -------
        <class 'pandas.core.frame.DataFrame'>

            --> A dataframe is returned, which includes several meta data on every tweet

        Example(s)
        ----------
        Obtains tweets from Donalds Trumps twitter timeline and creates a dataframe including several informations (listed above) on the tweets.

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> df = TweetAnalyzer().tweets_to_dataframe(tweets)
        """
        L = []
        for tweet in tweets:
            L.append([tweet.full_text, tweet.user.screen_name, tweet.created_at,
                                    tweet.retweeted_status.favorite_count if hasattr(tweet, 'retweeted_status') else tweet.favorite_count,
                                    tweet.retweet_count,
                                    ", ".join([hashtag_item['text'] for hashtag_item in tweet.entities['hashtags'] if tweet.entities["hashtags"]]),
                                    ", ".join([mention["screen_name"] for mention in tweet.entities['user_mentions'] if tweet.entities["user_mentions"]]),
                                    ", ".join([link['url'] for link in tweet.entities['urls'] if tweet.entities["urls"]]),
                                    tweet.id,
                                    "retweet" if hasattr(tweet, 'retweeted_status') else "tweet"
                                    ])
        return (pd.DataFrame(L, columns = ["tweets", "author", "date", "likes", "retweets", "hashtags", "linked_accounts", "urls", "id", "tweet_type"]))

######MERGE DATAFRAME##################################################################################################################################
    def merge_dataframe(self, df_tomerge, inplace = False):
        """
        Description
        -----------
        This function merges the dataframe in the object with other dataframes.

        Parameters
        ----------
        df_tomerge:         type = sequencial datatype (e.g list)
                            description = A list of dataframes one wants to merge.

        inplace:            type = boolean
                            description = If true, the existing object will be manipulated.
                                          Otherwise a new object will be created.
                            default = False
        Returns
        -------
        If inplace = True:
        None
            --> Existing object will be manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

            --> A new object is returned

        Example(s)
        ----------
        The following examples obtains Donald Trumps tweets on his timeline and merges older dataframes to it:

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.merge_dataframe(df_tomerge = [df_donaldtrump_2018, df_donaldtrump_2017], inplace = True)
            Without inplace
            >>>> tweet_analyzer2 = tweet_analyzer.merge_dataframe(df_tomerge = [df_donaldtrump_2018, df_donaldtrump_2017], inplace = True)
        """
        df = self.df.copy()
        for i in df_tomerge:
            df = pd.concat([self.df, i]).drop_duplicates().reset_index(drop=True)
        if inplace:
            self.df = df
        else:
            return TweetAnalyzer(self.tweets, df)
######GET - METHOD##################################################################################################################################
    def get_dataframe(self):
        """
        Description
        -----------
        This function returns the meta-dataframe of this class.

        Parameters
        ----------
        No parameters are passed.

        Returns
        -------
        <class 'pandas.core.frame.DataFrame'>

            --> A dataframe is returned, which includes several meta data on every tweet

        Example(s)
        ----------
        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.get_dataframe()
        """
        return self.df

######DATA IMPORT##################################################################################################################################
    def write_to_csv(self, *args, **kwargs):
        """
        Description
        -----------
        Write dataframe to a comma-separated values (csv) file.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
        """
        self.df.to_csv(*args, **kwargs)

    def write_to_json(self, *args, **kwargs):
        """
        Description
        -----------
        Convert the dataframe to a JSON string.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
        """
        self.df.to_json(*args, **kwargs)

    def write_to_excel(self, *args, **kwargs):
        """
        Description
        -----------
        Write dataframe to an Excel sheet.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
        """
        self.df.to_excel(*args, **kwargs)


    def read_from_csv(self, *args, **kwargs):
        """
        Description
        -----------
        Read a comma-separated values (csv) file into a dataframe.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        """
        self.df = pd.read_csv(*args, **kwargs)
        self.df.fillna("", inplace = True)
        self.df.date = pd.to_datetime(self.df.date)

    def read_from_json(self, *args, **kwargs):
        """
        Description
        -----------
        Convert a JSON string to a dataframe.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html
        """
        self.df = pd.read_json(*args, **kwargs)
        self.df.fillna("", inplace = True)
        self.df.date = pd.to_datetime(self.df.date)

    def read_from_excel(self, *args, **kwargs):
        """
        Description
        -----------
        Read an Excel file into a dataframe.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
        """
        self.df = pd.read_excel(*args, **kwargs)
        self.df.fillna("", inplace = True)
        self.df.date = pd.to_datetime(self.df.date)

######FILTER##################################################################################################################################
    def tweet_filter_hashtags(self, hashtags, all_in_one = False, reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to used hashtags.

        Parameters
        ----------
        hashtags:           type = list
                            description = A list of hashtags the user wants to filter for

        all_in_one:         type = boolean
                            description = If True, only tweets which contains all! hashtags in the list are obtained
                                      If False, tweets which contains one or more hashtags in the list are obtained
                            default = False

        reset_drop_index:   type = boolean
                            description = If True: the index of the filtered dataframe will be resetted and the old index dropped.
                                          If False: the index will not be manipulated.
                            default = True

        inplace:            type = boolean
                            description = If true, the existing object will be manipulated.
                                          Otherwise a new object will be created.
                            default = False

        Returns
        -------
        If inplace = True:
        None
            --> Existing object will be manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

            --> A new object is returned

        Example(s)
        ----------
        The following examples obtains Donald Trumps tweets on his timeline and filters according hashtags:

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_hashtags(df, ["chicago", "usa"], all_in_one = True, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_hashtags(["chicago", "usa"], all_in_one = True, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline which includes the hashtags: chicago and usa (if there are any)

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_hashtags(df, ["chicago", "usa"], all_in_one = False, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_hashtags(["chicago", "usa"], all_in_one = False, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline which includes the hashtags: chicago or usa or both (if there are any)
        """
        if "hashtags" not in self.df.columns:
            raise TypeError("Column hashtags does not exists!")
        if all_in_one:
            filtered_df = self.df.copy()
            for i in hashtags:
                filtered_df = filtered_df[filtered_df.hashtags.apply(lambda x: re.search("(?:^|\W)"+i+"(?:$|\W)",x) != None)]
            if reset_drop_index:
                filtered_df.reset_index(inplace=True, drop=True)
            if inplace:
                self.df = filtered_df
            else:
                return TweetAnalyzer(self.tweets, filtered_df)
        else:
            if (len(hashtags) == 1):
                filtered_df = self.df[self.df.hashtags.apply(lambda x: re.search("(?:^|\W)"+hashtags[0]+"(?:$|\W)",x) != None)]
                if reset_drop_index:
                    filtered_df.reset_index(inplace=True, drop=True)
                if inplace:
                    self.df = filtered_df
                else:
                    return TweetAnalyzer(self.tweets, filtered_df)
            else:
                filtered_df = self.df[self.df.hashtags.apply(lambda x: re.search("(?:^|\W)"+hashtags[0]+"(?:$|\W)",x) != None)]
                for i in range(1, len(hashtags)):
                    df_append = self.df[self.df.hashtags.apply(lambda x: re.search("(?:^|\W)"+hashtags[i]+"(?:$|\W)",x) != None)]
                    filtered_df = filtered_df.append(df_append)
                if reset_drop_index:
                    filtered_df.reset_index(inplace=True, drop=True)
                if inplace:
                    self.df = filtered_df
                else:
                    return TweetAnalyzer(self.tweets, filtered_df)

    def tweet_filter_likes(self, min_number_of_likes = 0, max_number_of_likes = None, reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to number of likes a tweet received.

        Parameters
        ----------
        min_number_of_likes:    type = int
                                description = The minimum number of likes a tweet should have
                                default = 0


        max_number_of_likes:    type = int or None
                                description = The maximum number of likes a tweet should have
                                              If None: No maximum number provided -> Everything >= min_number_of_likes is obtained
                                default = None

        reset_drop_index:       type = boolean
                                description = If True: the index of the filtered dataframe will be resetted and the old index dropped
                                              If False: the index will not be manipulated

        inplace:                type = boolean
                                description = If true, the existing object will be manipulated.
                                              Otherwise a new object will be created.
                                default = False

        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

            --> A new object is returned

        Example(s)
        ----------
        The following examples obtains Donald Trumps tweets on his timeline and filters according to the number of likes in a tweet.

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_likes(df, min_number_of_likes = 10, max_number_of_likes = 100, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_likes(min_number_of_likes = 10, max_number_of_likes = 100, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline having between 10 and 100 likes (if there are any)

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_likes(min_number_of_likes = 10, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_likes(min_number_of_likes = 10, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline having more or equal than 10 likes (if there are any)
        """
        if "likes" not in self.df.columns:
            raise TypeError("Column likes does not exists!")
        if max_number_of_likes == None:
            filtered_df = self.df[self.df.likes >= min_number_of_likes]
        else:
            filtered_df = self.df[(self.df.likes >= min_number_of_likes) & (self.df.likes <= max_number_of_likes)]
        if reset_drop_index:
            filtered_df.reset_index(inplace=True, drop=True)
        if inplace:
            self.df = filtered_df
        else:
            return TweetAnalyzer(self.tweets, filtered_df)

    def tweet_filter_retweets(self, min_number_of_retweets = 0, max_number_of_retweets = None, reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to retweets a tweet got.

        Parameters
        ----------
        min_number_of_retweets:     type = int
                                    description = The minimum number of retweets a tweet should have
                                    default = 0


        max_number_of_retweets:     type = int or None
                                    description = The maximum number of retweets a tweet should have
                                                  If None: No maximum number provided -> Everything >= min_number_of_retweets is obtained
                                    default = None

        reset_drop_index:           type = boolean
                                    description = If True: the index of the filtered dataframe will be resetted and the old index dropped
                                                  If False: the index will not be manipulated

        inplace:                    type = boolean
                                    description = If true, the existing object will be manipulated.
                                                  Otherwise a new object will be created.
                                    default = False


        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

            --> A new object is returned

        Example(s)
        ----------
        The following examples obtains Donald Trumps tweets on his timeline and filters according to the number of retweets.

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_likes(min_number_of_retweets = 10, max_number_of_retweets = 100, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_likes(min_number_of_retweets = 10, max_number_of_retweets = 100, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline having between 10 and 100 retweets (if there are any)

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer..tweet_filter_likes(min_number_of_retweets = 10, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_likes(min_number_of_retweets = 10, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline having more or equal than 10 retweets (if there are any)
        """
        if "retweets" not in self.df.columns:
            raise TypeError("Column retweets does not exists!")

        if max_number_of_retweets == None:
            filtered_df = self.df[self.df.retweets >= min_number_of_retweets]
        else:
            filtered_df = self.df[(self.df.retweets >= min_number_of_retweets) & (self.df.retweets <= max_number_of_retweets)]

        if reset_drop_index:
            filtered_df.reset_index(inplace=True, drop=True)
        if inplace:
            self.df = filtered_df
        else:
            return TweetAnalyzer(self.tweets, filtered_df)

    def tweet_filter_hyperlink_usage(self, no_hyperlinks = True, reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to the use of hyperlinks in a tweet.

        Parameters
        ----------
        no_hyperlinks:              type = Bool
                                    description = If True: Only tweets without an url are obtained
                                                  If False: Only tweets with an url are obtained (the opposite)
                                    default = True

        reset_drop_index:           type = boolean
                                    description = If True: the index of the filtered dataframe will be resetted and the old index dropped
                                                  If False: the index will not be manipulated

        inplace:                    type = boolean
                                    description = If true, the existing object will be manipulated.
                                                  Otherwise a new object will be created.
                                    default = False

        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

        Example(s)
        ----------
        The following examples obtains Donald Trumps tweets on his timeline and filters according the usage of hyperlinks

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_hyperlink_usage(no_hyperlinks = False, inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_hyperlink_usage(no_hyperlinks = False, inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline having urls in it (if there are any)

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_hyperlink_usage(inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_hyperlink_usage(inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline having no urls in it (if there are any)
        """
        if "urls" not in self.df.columns:
            raise TypeError("Column hashtags does not exists!")

        if no_hyperlinks:
            filtered_df = self.df[self.df.urls.apply(lambda x: bool(x) == False)]
        else:
            filtered_df = self.df[self.df.urls.apply(lambda x: bool(x) == True)]
        if reset_drop_index:
            filtered_df.reset_index(inplace=True, drop=True)
        if inplace:
            self.df = filtered_df
        else:
            return TweetAnalyzer(self.tweets, filtered_df)

    def tweet_filter_dates(self, start_date, end_date, reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to a given daterange.

        Parameters
        ----------
        start_date:                 type = str
                                    description = A date representation in the following format: "YEAR-MONTH-DAY", representing the start date
                                                  from when one wants to obtain the tweets

        end_date:                   type = str
                                    description = A date representation in the following format: "YEAR-MONTH-DAY", representing the end date
                                                  to when one wants to obtain the tweets

        reset_drop_index:           type = boolean
                                    description = If True: the index of the filtered dataframe will be resetted and the old index dropped
                                                  If False: the index will not be manipulated

        inplace:                    type = boolean
                                    description = If true, the existing object will be manipulated.
                                                  Otherwise a new object will be created.
                                    default = False

        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

        Example(s)
        ----------
        The following examples obtains Donald Trumps tweets on his timeline and filters between two dates

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_dates(df, start_date = "2019-01-01", end_date = "2019-05-31", inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_dates(df, start_date = "2019-01-01", end_date = "2019-05-31", inplace = False)

            Obtains tweets from Donalds Trumps twitter timeline between the 1. January 2019 to 31. May 2019 (if there are any)
        """
        if "date" not in self.df.columns:
            raise TypeError("Column date does not exists!")

        filtered_df = self.df[(self.df.date >= start_date) & (self.df.date < end_date)]
        if reset_drop_index:
            filtered_df.reset_index(inplace=True, drop=True)
        if inplace:
            self.df = filtered_df
        else:
            return TweetAnalyzer(self.tweets, filtered_df)

    def tweet_filter_account(self, accountname, reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to given accountnames.

        Parameters
        ----------
        accountname:                type = Sequential data type, e.g. List
                                    description = List of account names

        reset_drop_index:           type = boolean
                                    description = If True: the index of the filtered dataframe will be resetted and the old index dropped
                                                  If False: the index will not be manipulated

        inplace:                    type = boolean
                                    description = If true, the existing object will be manipulated.
                                                  Otherwise a new object will be created.
                                    default = False

        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

        Example(s)
        ----------
        The following examples obtains Donald Trumps and Barack Obamas tweets on their timeline and filtering only for Donald Trumps tweets:

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_account(df, accountname = ["realDonaldTrump"], inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_account(df, accountname = ["realDonaldTrump"], inplace = False)

            Obtains only tweets from Donalds Trumps twitter timeline by filtering out the Barack Obama timeline (if there are any)
        """
        if "author" not in self.df.columns:
            raise TypeError("Column author does not exists!")

        if (len(accountname) == 1):
            filtered_df = self.df[self.df.author.apply(lambda x: accountname[0] == x)]
            if reset_drop_index:
                filtered_df.reset_index(inplace=True, drop=True)
            if inplace:
                self.df = filtered_df
            else:
                return TweetAnalyzer(self.tweets, filtered_df)
        else:
            filtered_df = self.df[self.df.author.apply(lambda x: accountname[0] == x)]
            for i in range(1, len(accountname)):
                df_append = self.df[self.df.author.apply(lambda x: accountname[i] == x)]
                filtered_df = filtered_df.append(df_append)
            if reset_drop_index:
                filtered_df.reset_index(inplace=True, drop=True)
            if inplace:
                self.df = filtered_df
            else:
                return TweetAnalyzer(self.tweets, filtered_df)

    def tweet_filter_tweet_type(self, obtain = "tweets", reset_drop_index = True, inplace = False):
        """
        Description
        -----------
        This function filters the meta data dataframe according to a given tweet type.

        Parameters
        ----------
        obtain:                     type = str
                                    description = The tweet type one wants to obtain.
                                                  "tweets": Obtain only tweets
                                                  "retweets": Obtain oly retweets
                                    default = "tweets"

        reset_drop_index:           type = boolean
                                    description = If True: the index of the filtered dataframe will be resetted and the old index dropped
                                                  If False: the index will not be manipulated

        inplace:                    type = boolean
                                    description = If true, the existing object will be manipulated.
                                                  Otherwise a new object will be created.
                                    default = False

        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

        Example(s)
        ----------
        The following example obtains Donald Trumps tweets on his timeline and filters according to tweets

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_tweet_type(obtain = "tweets", inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_tweet_type(obtain = "tweets", inplace = False)


        The following example obtains Donald Trumps tweets on his timeline and filters according to retweets

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_filter_tweet_type(obtain = "retweets", inplace = True)
            Without inplace:
            >>>> tweet_analyzer2 = tweet_analyzer.tweet_filter_tweet_type(obtain = "retweets", inplace = False)
        """
        if "tweet_type" not in self.df.columns:
            raise TypeError("Column hashtags does not exists!")

        if obtain == "tweets":
            filtered_df = self.df[self.df.tweet_type.apply(lambda x: "retweet" not in x)]
        elif obtain == "retweets":
            filtered_df = self.df[self.df.urls.apply(lambda x: "retweet" in x)]
        else:
            raise TypeError('filter tweet_filter_tweet_type Error: Parameter "obtain" not correctly specified')

        if reset_drop_index:
            filtered_df.reset_index(inplace=True, drop=True)
        if inplace:
            self.df = filtered_df
        else:
            return TweetAnalyzer(self.tweets, filtered_df)

######TWEET MANIPULATION##################################################################################################################################
    def tweet_manipulation(self, all_tweets = True, tweetnumber=0,delete_htmlent=True,
        delete_hyperlinks=False,delete_numbers=False, delete_hashtags=False,
        only_small_letters=False, delete_diamonds_from_hashtags=False,
        delete_accountlinks=False, delete_at_from_accountlinks=False,
        inplace = False):
        """
        Description
        -----------
        Manipulates the tweets column in the dataframe either by a given index number or as a whole.

        Parameters
        ----------
        all_tweets:                         type = boolean
                                            description = If True: All tweets are manipulated.
                                                          If False: A single tweet is manipulated.
                                            default = True

        tweetnumber:                        type = int
                                            description = If "all-tweets" is True: The index number of the tweet, which should be manipulated.
                                            default =  False
        delete_htmlent:                     type = boolean
                                            description = If True: Deletes HTML Enteties from twitter-tweet(s).
                                            default = True
        delete_hyperlinks:                  type = boolean
                                            description = If True: Deletes hyperlinks from twitter-tweet(s).
                                            default = False

        delete_numbers:                     type = boolean
                                            description = If True: Deletes numbers from twitter-tweet(s).
                                            default = False

        delete_hashtags:                    type = boolean
                                            description = If True: Deletes hashtags from twitter-tweet(s).
                                            default = False

        only_small_letters:                 type = boolean
                                            description = If True: Changes every big letter to a small letter in twitter-tweet(s).
                                            default = False

        delete_accountlinks:                type = boolean
                                            description = If True: Deletes account links from twitter-tweet(s).
                                            default = False

        delete_at_from_accountlinks:        type = boolean
                                            description = If True: Deletes the '@' from twitter-tweet(s)
                                            default = False


        delete_diamonds_from_hashtags:      type = boolean
                                            description = If True: Deletes diamonds from hashtags from twitter-tweet(s)
                                            default = False

        inplace:                            type = boolean
                                            description = If true, the existing object will be manipulated.
                                                          Otherwise a new object will be created.
                                            default = False
        Returns
        -------
        If inplace = True:
        None
            --> Existing object will me manipulated

        Otherwise:
        <class 'tweet_analyzer.TweetAnalyzer'>

        Example(s)
        ----------
        The following examples obtains Donald Trumps and Barack Obamas tweets and deletes hyperlinks, hashtags, accountlinks, numbers as well as changes big to small letters

        1.  (ALL TWEETS)
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_manipulation(all_tweets = True, only_small_letters=True,
                                                   delete_hyperlinks=True , delete_hashtags=True, delete_accountlinks =True, delete_numbers=True, inplace = True)
            Without inplace:
            >>>> cleaned_object = tweet_analyzer.tweet_manipulation(all_tweets = True, only_small_letters=True,
                                                                    delete_hyperlinks=True , delete_hashtags=True, delete_accountlinks =True, delete_numbers=True, inplace = False)

        2.  (SINGLE TWEET)
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.tweet_manipulation(all_tweets = False, tweetnumber = 10 ,only_small_letters=True,
                                                   delete_hyperlinks=True , delete_hashtags=True, delete_accountlinks =True, delete_numbers=True, inplace = True)
            Without inplace:
            >>>> cleaned_object = tweet_analyzer.tweet_manipulation(all_tweets = False, tweetnumber = 10, only_small_letters=True,
                                                                    delete_hyperlinks=True , delete_hashtags=True, delete_accountlinks =True, delete_numbers=True, inplace = False)
        """
        filtered_df = self.df.copy()
        if all_tweets:
            if delete_htmlent:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace('<[^<]+?>', '')
                filtered_df["tweets"] = filtered_df["tweets"].str.replace("&amp;+|&lt;+|&gt;+|&quot;+|&apos;+", '')
            if delete_hyperlinks:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''," ", regex=True)
            if delete_numbers:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace('[0-9]+', '')
            if delete_hashtags:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace('#\S+\s*','')
            if only_small_letters:
                filtered_df["tweets"] = filtered_df["tweets"].str.lower()
            if delete_diamonds_from_hashtags:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace('#+', '')
            if delete_accountlinks:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace('@\S+\s*','')
            if delete_at_from_accountlinks:
                filtered_df["tweets"] = filtered_df["tweets"].str.replace('@+', '')
            if inplace:
                self.df = filtered_df
            else:
                return TweetAnalyzer(self.tweets, filtered_df)
        else:
            text=filtered_df.tweets.iloc[tweetnumber]
            if delete_htmlent:
                text=re.sub('<[^<]+?>', '', text) #Cleaning HTML-Entetiee.
                text=re.sub("&amp;+|&lt;+|&gt;+|&quot;+|&apos;+", '', text)
            if delete_hyperlinks:
                text=re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''," ", text)
            if delete_numbers:
                text=re.sub('[0-9]+', '',text)
            if delete_hashtags:
                text=re.sub('#\S+\s*','',text)
            if only_small_letters:
                text=text.lower()
            if delete_diamonds_from_hashtags:
                text=re.sub('#+', '', text)
            if delete_accountlinks:
                text=re.sub('@\S+\s*','',text)
            if delete_at_from_accountlinks:
                text=re.sub('@+', '', text)
            filtered_df.at[tweetnumber, 'tweets'] = text
            if inplace:
                self.df = filtered_df
            else:
                return TweetAnalyzer(self.tweets, filtered_df)

######FREQUENCY COUNT##################################################################################################################################
    def bagofwords(self, on = "tweets", extended_view = True, stopOWN=[]):
        """
        Description
        -----------
        Cleans the Dataframe and returns a new dataframe which has all words as Column and shows the
        vector of every single tweet.

        Parameters
        ----------
        on:                         type = str
                                    description = The column, one wants to obtain a frequency count (bagofwords-representation) from.
                                    default = "tweets"

        extended_view:              type = boolean
                                    description = If true: Extended Dataframe, showing frequency for every tweet.
                                                  If False: Summed wordcount, sorted in descending order.
                                    default =  False

        stopOWN:                    type = <class 'list'>
                                    description = List of words, you want to delete from the frequency count.
                                    default = False

        Returns
        -------
        <class 'pandas.core.frame.DataFrame'>

            --> A dataframe is returned, which includes a frequency count of the specified column ("on"-parameter)
                either as an extended view or compressed view ("extended_view" - parameter)

        Example(s)
        ----------
        The following examples obtains Donald Trumps and Barack Obamas tweets and get a frequency_count of the used words in their tweets

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.bagofwords(on="tweets", extended_view = False)

        The following examples obtains Donald Trumps and Barack Obamas tweets and get a frequency_count of the used hashtags in their tweets

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.bagofwords(on="hashtags", extended_view = True)

        """
        stopDE =['unsere', 'anderes', 'ist', 'andern', 'hab', 'welche', 'dasselbe', 'jener', 'ich', 'indem', 'solchem', 'manchem', 'während', 'anderm', 'einig', 'kann', 'keines', 'seinen', 'so', 'aber', 'jenen', 'von', 'zur', 'jenes', 'solches', 'diese', 'seinem', 'derselben', 'einmal', 'jedes', 'eurem', 'sollte', 'manchen', 'keiner', 'ob', 'dessen', 'einer', 'sich', 'können', 'allem', 'doch', 'einem', 'waren', 'er', 'nur', 'aus', 'deine', 'wo', 'andere', 'welches', 'nichts', 'wie', 'aller', 'hier', 'desselben', 'keinen', 'meiner', 'meine', 'dieses', 'zwar', 'noch', 'anderem', 'bin', 'unser', 'wenn', 'ander', 'allen', 'gegen', 'diesen', 'weil', 'eurer', 'weiter', 'keinem', 'an', 'haben', 'meinem', 'dieselbe', 'und', 'derer', 'wollen', 'durch', 'eines', 'denn', 'musste', 'welchen', 'hatte', 'war', 'damit', 'keine', 'mein', 'dieser', 'eures', 'wirst', 'würde', 'einiger', 'dass', 'nach', 'anders', 'jetzt', 'soll', 'deines', 'demselben', 'auf', 'euren', 'für', 'muss', 'dazu', 'machen', 'wollte', 'ihrem', 'den', 'selbst', 'dich', 'jeden', 'dir', 'also', 'bis', 'jene', 'in', 'mich', 'sind', 'würden', 'seines', 'im', 'wird', 'viel', 'unserem', 'solcher', 'zum', 'ihn', 'könnte', 'warst', 'ihm', 'auch', 'bist', 'dem', 'ohne', 'sie', 'vor', 'dort', 'da', 'das', 'die', 'etwas', 'mancher', 'jenem', 'hatten', 'hin', 'ihr', 'kein', 'sein', 'sehr', 'dann', 'mit', 'weg', 'was', 'ins', 'seiner', 'euer', 'sondern', 'jeder', 'ihren', 'daß', 'um', 'dein', 'meinen', 'einen', 'ihrer', 'solche', 'unseres', 'mir', 'anderen', 'dies', 'du', 'eine', 'meines', 'unter', 'deinem', 'einige', 'werde', 'wieder', 'anderer', 'hinter', 'als', 'welchem', 'ihnen', 'einigem', 'manches', 'seine', 'über', 'man', 'hat', 'anderr', 'ein', 'am', 'jedem', 'unseren', 'wir', 'deinen', 'bei', 'derselbe', 'gewesen', 'will', 'welcher', 'nicht', 'eure', 'des', 'werden', 'euch', 'oder', 'alles', 'zu', 'einiges', 'habe', 'uns', 'alle', 'der', 'einigen', 'ihre', 'jede', 'nun', 'denselben', 'sonst', 'diesem', 'vom', 'dieselben', 'ihres', 'manche', 'zwischen', 'solchen', 'deiner', 'es']
        stopENG =['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers','herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which','who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been','being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if','or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',         'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out','on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',         'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not','only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',         "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",         'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        stopwords= stopDE+stopENG+stopOWN
        if on == "tweets":
            if "tweets" not in self.df.columns:
                raise TypeError("Column tweets does not exists!")
            cleaned_object = self.tweet_manipulation(only_small_letters=True, delete_hyperlinks=True , delete_hashtags=True, delete_accountlinks =True, delete_numbers=True)
            vectorizer = CountVectorizer()
            vectorizer.stop_words = stopwords
            vectorizer.fit(cleaned_object.get_dataframe().tweets)
            dtm = vectorizer.transform(cleaned_object.get_dataframe().tweets)
            transformed_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names())
            if extended_view:
                return transformed_df
            else:
                transformed_df_c = transformed_df.sum().sort_values(ascending=False).to_frame().reset_index().rename(
                                    columns={"index": "words", 0: "count"})
                transformed_df_c['index'] = transformed_df_c.index + 1
                transformed_df_c['index_perc'] = 100*transformed_df_c['index']/transformed_df_c.iloc[-1]['index']
                return transformed_df_c
        elif on == "hashtags":
            if "hashtags" not in self.df.columns:
                raise TypeError("Column hashtags does not exists!")
            vectorizer = CountVectorizer()
            vectorizer.fit(self.df.hashtags)
            dtm = vectorizer.transform(self.df.hashtags)
            transformed_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names())
            if extended_view:
                return transformed_df
            else:
                transformed_df_c = transformed_df.sum().sort_values(ascending=False).to_frame().reset_index().rename(
                        columns={"index": "hashtags", 0: "count"})
                transformed_df_c['index'] = transformed_df_c.index + 1
                transformed_df_c['index_perc'] = 100*transformed_df_c['index']/transformed_df_c.iloc[-1]['index']
                return transformed_df_c
        elif on == "linked_accounts":
            if "linked_accounts" not in self.df.columns:
                raise TypeError("Column linked_accounts does not exists!")
            vectorizer = CountVectorizer()
            vectorizer.fit(self.df.linked_accounts)
            dtm = vectorizer.transform(self.df.linked_accounts)
            transformed_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names())
            if extended_view:
                return transformed_df
            else:
                transformed_df_c = transformed_df.sum().sort_values(ascending=False).to_frame().reset_index().rename(
                        columns={"index": "accounts", 0: "count"})
                transformed_df_c['index'] = transformed_df_c.index + 1
                transformed_df_c['index_perc'] = 100*transformed_df_c['index']/transformed_df_c.iloc[-1]['index']
                return transformed_df_c
        else:
            raise TypeError("Remember: You can only get a frequency count of the tweets, hashtags and linked accounts!")


######GRAPHICAL REPRESENTATION##################################################################################################################################
    def  plot_bar(self, type, windowsize=(10,5), stopOWN =[], plotstyle = "ggplot", count = 10, percent = 15.0,
                    title = None, xvalues = False, facecolor = "blue", edgecolor = "blue", alpha=0.5, fontfamily = "sans", font=12):
        """
        Description
        -----------
        Plots a bar chart with either most frequently used words or most frequently linked accounts.

        Parameters
        -----------
        type:                       type = str
                                    'wct' = displays most common words, based on count
                                    'wpt' = displays most common words, by percentage
                                    'la_ct' = displays most linked accounts, by count
                                    'la_pt' = displays most linked accounts, by percentage
                                    'hashtags' = displays most common hashtags, by count

        windowsize:                 type = tuple
                                    description = sets windowsize in inches
                                    default = (10,5)

        plotstyle:                  type = matplotlib style sheet (str).
                                    default = "ggplot"

        count:                      type = integer
                                    description = returns top n entries
                                    default = 10

        percent:                    type = float
                                    description = returns top n% entries
                                    default = 15.0

        title:                      type = str
                                    description = plot title
                                    default = 'Top x most used words'

        xvalues:                    type = boolean
                                    description = True to show values for the bars
                                    default = False

        facecolor:                  type = matplotlib color (str)
                                    description = color of bars
                                    default = 'blue'

        edgecolor:                  type = matplotlib color (str)
                                    description = color of bar edges
                                    default = 'blue'

        alpha:                      type = float
                                    description = sets opacity of the color bars
                                    default = 0.5

        fontfamily:                 type = font type (str)
                                    description = sets font of title
                                    default = "sans"

        font:                       type = int
                                    description = Setting the font size of the title, x and y label
                                    default = 12

        Returns
        -----------
        <none>

            --> diplays chart

        Examples
        -----------
        1.
            >>>> Parties = ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei","cdu","csu"]
            >>>> twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, Parties)
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-07-03", end_date = "2019-07-07")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.plot_bar(type="wct", count=20)
        """
        if type == 'wct':
            wordcountframe = self.bagofwords(extended_view = False, stopOWN = stopOWN)
            wordcountframe = wordcountframe[wordcountframe["index"] <= count]
            if title == None:
                title = 'Top ' + str(wordcountframe["index"].max()) + ' most used words'
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            rects = plt.barh(wordcountframe["words"], wordcountframe["count"], color=facecolor, edgecolor=edgecolor, alpha=alpha)
            if xvalues:
                c = 0
                for rect in rects:
                    plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                    c += 1
            plt.title(title,fontfamily=fontfamily,fontsize=font)
            plt.xlabel('Frequency',fontsize=font)
            plt.ylabel('Words',fontsize=font)
            plt.show()
        elif type == 'wpt':
            wordcountframe = self.bagofwords(extended_view = False, stopOWN=stopOWN)
            wordcountframe = wordcountframe[wordcountframe.index_perc <= percent]
            if title == None:
                title = 'Top ' + str(percent) + '% most used words'
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            rects = plt.barh(wordcountframe["words"], wordcountframe["count"], color=facecolor, edgecolor=edgecolor,alpha=alpha)
            if xvalues:
                c = 0
                for rect in rects:
                    plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                    c += 1
            plt.title(title, fontfamily=fontfamily, fontsize=font)
            plt.xlabel('Frequency',fontsize=font)
            plt.ylabel('Words',fontsize=font)
            plt.show()
        elif type == 'la_ct':
            wordcountframe = self.bagofwords(on = "linked_accounts", extended_view = False, stopOWN=stopOWN)
            wordcountframe = wordcountframe[wordcountframe["index"] <= count]
            if title == None:
                title = 'Top ' + str(wordcountframe["index"].max()) + ' most linked accounts'
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            rects = plt.barh(wordcountframe["accounts"], wordcountframe["count"], color=facecolor, edgecolor=edgecolor, alpha=alpha)
            if xvalues:
                c = 0
                for rect in rects:
                    plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                    c += 1
            plt.title(title, fontfamily=fontfamily)
            plt.xlabel('Frequency')
            plt.ylabel('Accounts')
            plt.show()
        elif type == 'la_pt':
            wordcountframe = self.bagofwords(on = "linked_accounts", extended_view = False, stopOWN=stopOWN)
            wordcountframe = wordcountframe[wordcountframe.index_perc <= percent]
            if title == None:
                title = 'Top ' + str(percent) + '% most linked accounts'
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            rects = plt.barh(wordcountframe["accounts"], wordcountframe["count"], color=facecolor, edgecolor=edgecolor, alpha=alpha)
            if xvalues:
                c = 0
                for rect in rects:
                    plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                    c += 1
            plt.title(title, fontfamily=fontfamily, fontsize=font)
            plt.xlabel('Frequency',fontsize=font)
            plt.ylabel('Accounts',fontsize=font)
            plt.show()
        elif type == 'hashtags':
            wordcountframe = self.bagofwords(on = "hashtags", extended_view = False)
            wordcountframe = wordcountframe[wordcountframe["index"] <= count]
            if title == None:
                title = 'Top ' + str(wordcountframe["index"].max()) + ' most common hashtags'
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            rects = plt.barh(wordcountframe["hashtags"], wordcountframe["count"],color=facecolor, edgecolor=edgecolor, alpha=alpha)
            if xvalues:
                c = 0
                for rect in rects:
                    plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                    c += 1
            plt.title(title,fontfamily=fontfamily, fontsize=font)
            plt.xlabel('Frequency', fontsize=font)
            plt.ylabel('Hashtags', fontsize=font)
            plt.show()
        else:
            raise TypeError('plot_bar Error: type not specified')

    def plot_bar_sum(self, type = "count", title = None, facecolor = "blue", edgecolor = "black",xvalues = False, alpha = 0.5, stacked = False,
                    return_df = False, sort_val = True, windowsize = (10,5), colormap = "coolwarm", colordict = None, plotstyle = "ggplot", font=12):
        """
        Description
        -----------
        Plots a bar chart of the summed retweets, likes, tweetcount.

        Parameters
        -----------
        type:                       type = str
                                    'count' = display bar chart of summed tweet count.
                                    'likes' = displays bar chart of summed likes.
                                    'retweets' = displays bar chart of summed retweets.

        windowsize:                 type = tuple
                                    description = sets windowsize in inches
                                    default = (10,5)

        plotstyle:                  type = matplotlib style sheet.
                                    default = "ggplot"

        title:                      type = str
                                    description = plot title
                                    default = 'Top x most used words'

        xvalues:                    type = boolean
                                    description = True to show values for the bars
                                    default = False

        facecolor:                  type = matplotlib color (str)
                                    description = color of bars
                                    default = 'blue'

        edgecolor:                  type = matplotlib color (str)
                                    description = color of bar edges
                                    default = 'blue'

        alpha:                      type = float
                                    description = sets opacity of the color bars
                                    default = 0.5

        stacked:                    type = boolean
                                    description = if one imported tweets and retweets, he can procude a stacked bar chart
                                    default = False

        return_df:                  type = boolean
                                    description = returns the dataframe, the plot is based on
                                    default = False

        sort_val:                   type = boolean
                                    description = sort values in bar graph
                                    default = True

        colormap:                   type = str
                                    description = Specify a colormap for the stacked bar chart, does not work on normal bar charts: Use facecolor thereself.
                                    default = "coolwarm"

        colordict:                  type = dict
                                    description = Specify a dictionary with the xlabels as keys and the color as values. The xlabels will be colored accordingly
                                    default = None

        font:                       type = int
                                    description = Setting the font size of the title, x and y label
                                    default = 12

        Returns
        -----------
        if return_df = False:

        <none>

            --> diplays chart

        if return_df = True

        <class 'pandas.core.frame.DataFrame'>

            --> dataframe on which the graph is based

        Examples
        -----------
        1.
            >>>> Parties = ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei","cdu","csu"]
            >>>> twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, Parties)
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-07-03", end_date = "2019-07-07")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> colordict = {'fwlandtag':"green", "CSU":"red", "fdp":"green", "Die_Gruenen":"green", "spdde":"red", "dieLinke":"red", "CDU":"red", "DiePARTEI":"green", "AfD":"green"}
            >>>> tweet_analyzer.plot_bar_sum(type="retweets", stacked= False, sort_val = True, xvalues = True, colordict = colordict)
        """
        if stacked == True:
            df = self.df.copy()
            df["count"] = 1
            plt.style.use(plotstyle)
            df_grp = df.groupby(["author", "tweet_type"])["likes", "retweets","count"].sum().unstack().fillna(0)
            if type == "count":
                df_count = df_grp["count"].copy()
                if sort_val:
                    df_count["total"] = df_count["retweet"]+df_count["tweet"]
                    df_count.sort_values(by=["total"], inplace = True)
                ax = df_count[["retweet", "tweet"]].plot(kind="barh", stacked=True, figsize=windowsize, alpha = alpha, colormap = colormap)
                if colordict != None:
                    for ytick in ax.get_yticklabels():
                        ytick.set_color("white")
                        for key, value in colordict.items():
                            if ytick.get_text()==key:
                                bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                                plt.setp(ytick, bbox=bbox)
                if xvalues:
                    totals = []
                    for i in ax.patches:
                        totals.append(i.get_width())
                    total = sum(totals)
                    for i in ax.patches:
                        if (((i.get_width()/total)*100) < 0.5):
                            pass
                        else:
                            ax.text(i.get_width()-(i.get_width()-i.get_x()), i.get_y()-.30, \
                                    str(int(i.get_width())), fontsize=10, color='dimgrey')
                if title == None:
                    plt.title('Sum of Tweets',fontsize=font)
                else:
                    plt.title(title,fontsize=font)
                plt.xlabel("Count",fontsize=font)
                plt.ylabel('Accounts',fontsize=font)
                plt.legend(loc = "lower right")
                plt.show()
                if return_df:
                    return df_count
            elif type == "likes":
                df_likes = df_grp["likes"].copy()
                if sort_val:
                    df_likes["total"] = df_likes["retweet"]+df_likes["tweet"]
                    df_likes.sort_values(by=["total"], inplace = True)
                ax = df_likes[["retweet", "tweet"]].plot(kind="barh", stacked=True, figsize=windowsize, alpha = alpha, colormap = colormap)
                if colordict != None:
                    for ytick in ax.get_yticklabels():
                        ytick.set_color("white")
                        for key, value in colordict.items():
                            if ytick.get_text()==key:
                                bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                                plt.setp(ytick, bbox=bbox)
                if xvalues:
                    totals = []
                    for i in ax.patches:
                        totals.append(i.get_width())
                    total = sum(totals)
                    for i in ax.patches:
                        if (((i.get_width()/total)*100) < 0.5):
                            pass
                        else:
                            ax.text(i.get_width()-(i.get_width()-i.get_x()), i.get_y()-.30, \
                                    str(int(i.get_width())), fontsize=10, color='dimgrey')
                if title == None:
                    plt.title('Sum of Likes',fontsize=font)
                else:
                    plt.title(title,fontsize=font)
                plt.xlabel('Likes',fontsize=font)
                plt.ylabel('Accounts',fontsize=font)
                plt.legend(loc = "lower right")
                plt.show()
                if return_df:
                    return df_likes
            elif type == "retweets":
                df_retweets = df_grp["retweets"].copy()
                if sort_val:
                    df_retweets["total"] = df_retweets["retweet"]+df_retweets["tweet"]
                    df_retweets.sort_values(by=["total"], inplace = True)
                ax = df_retweets[["retweet", "tweet"]].plot(kind="barh", stacked=True, figsize=windowsize, alpha = alpha, colormap = colormap)
                if colordict != None:
                    for ytick in ax.get_yticklabels():
                        ytick.set_color("white")
                        for key, value in colordict.items():
                            if ytick.get_text()==key:
                                bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                                plt.setp(ytick, bbox=bbox)
                if xvalues:
                    totals = []
                    for i in ax.patches:
                        totals.append(i.get_width())
                    total = sum(totals)
                    for i in ax.patches:
                        if (((i.get_width()/total)*100) < 0.5):
                            pass
                        else:
                            ax.text(i.get_width()-(i.get_width()-i.get_x()), i.get_y()-.30, \
                                    str(int(i.get_width())), fontsize=10, color='dimgrey')
                if title == None:
                    plt.title('Sum of Retweets',fontsize=font)
                else:
                    plt.title(title,fontsize=font)
                plt.xlabel('Retweets',fontsize=font)
                plt.ylabel('Accounts',fontsize=font)
                plt.legend(loc = "lower right")
                plt.show()
                if return_df:
                    return df_retweets
            else:
                raise TypeError('plot_bar_sum Error: type not specified')
        else:
            df = self.df.copy()
            df["count"] = 1
            plt.style.use(plotstyle)
            fig, ax = plt.subplots(figsize = windowsize)
            df_grp = df.groupby("author")["likes", "retweets","count"].sum()
            if type == "count":
                if sort_val:
                    df_grp.sort_values(by=["count"], inplace =True)
                rects = plt.barh(df_grp.index, df_grp["count"], color = facecolor, edgecolor = edgecolor, alpha = alpha)
                ax.set_yticklabels(df_grp.index)
                if colordict != None:
                    for ytick in ax.get_yticklabels():
                        ytick.set_color("white")
                        for key, value in colordict.items():
                            if ytick.get_text()==key:
                                bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                                plt.setp(ytick, bbox=bbox)
                if xvalues:
                    c = 0
                    for rect in rects:
                        plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                        c += 1
                if title == None:
                    plt.title('Sum of Tweets',fontsize=font)
                else:
                    plt.title(title,fontsize=font)
                plt.xlabel('Count',fontsize=font)
                plt.ylabel('Accounts',fontsize=font)
                plt.show()
                if return_df:
                    return df_grp
            elif type == "likes":
                if sort_val:
                    df_grp.sort_values(by=["likes"], inplace =True)
                rects = plt.barh(df_grp.index, df_grp["likes"], color=facecolor, edgecolor=edgecolor, alpha=alpha)
                ax.set_yticklabels(df_grp.index)
                if colordict != None:
                    for ytick in ax.get_yticklabels():
                        ytick.set_color("white")
                        for key, value in colordict.items():
                            if ytick.get_text()==key:
                                bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                                plt.setp(ytick, bbox=bbox)
                if xvalues:
                    c = 0
                    for rect in rects:
                        plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                        c += 1
                if title == None:
                    plt.title('Sum of Likes', fontsize=font)
                else:
                    plt.title(title, fontsize=font)
                plt.xlabel('Likes', fontsize=font)
                plt.ylabel('Accounts', fontsize=font)
                plt.show()
                if return_df:
                    return df_grp
            elif type == "retweets":
                if sort_val:
                    df_grp.sort_values(by=["retweets"], inplace =True)
                rects = plt.barh(df_grp.index, df_grp["retweets"], color = facecolor, edgecolor = edgecolor, alpha = alpha)
                ax.set_yticklabels(df_grp.index)
                if colordict != None:
                    for ytick in ax.get_yticklabels():
                        ytick.set_color("white")
                        for key, value in colordict.items():
                            if ytick.get_text()==key:
                                bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                                plt.setp(ytick, bbox=bbox)
                if xvalues:
                    c = 0
                    for rect in rects:
                        plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                        c += 1
                if title == None:
                    plt.title('Sum of Retweets', fontsize=font)
                else:
                    plt.title(title, fontsize=font)
                plt.xlabel('Retweets', fontsize=font)
                plt.ylabel('Accounts', fontsize=font)
                plt.show()
                if return_df:
                    return df_grp
            else:
                raise TypeError('plot_bar_sum Error: type not specified')

    def wordcloud(self, type = "tweets", stopOWN = [], windowsize = (20,11.25), color='white'):
        """
        Description
        -----------
        Plots a wordcloud of the most common words, hashtags, linked accounts.

        Parameters
        -----------
        type:                       type = str
                                    'tweets' = displays most common words
                                    'hashtag' = displays most common hashtags
                                    'linked_accounts' = displays most linked accounts

        windowsize:                 type = tuple
                                    description = sets windowsize in inches
                                    default = (20,11.25)

        stopOWN:                    type = <class 'list'>
                                    description = List of words, you want to delete from the frequency count.
                                    default = False
        color:                      type = str
                                    description = sets backgroundcolor
                                    default = "white"
        Returns
        -----------
        <none>

            --> diplays chart

        Examples
        -----------
        1.
            >>>> Parties = ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei","cdu","csu"]
            >>>> twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, Parties)
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-07-03", end_date = "2019-07-07")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.wordcloud(type="tweets", stopOWN = ["hi", "rt"])
        """
        from wordcloud import WordCloud
        if type == "tweets":
            bagframe = self.bagofwords(on='tweets', extended_view=False, stopOWN = stopOWN)
            bagframe = bagframe.set_index('words')
            dict1 = bagframe["count"].to_dict()
            wc = WordCloud(width = 1920, height = 1080, background_color=color)
            wc.generate_from_frequencies(dict1)
            plt.figure(figsize=windowsize)
            plt.axis("off")
            plt.imshow(wc, interpolation="bilinear",aspect='auto')
            plt.show()
        elif type == "hashtags":
            bagframe = self.bagofwords(on='hashtags', extended_view=False, stopOWN = stopOWN)
            bagframe = bagframe.set_index('hashtags')
            dict1 = bagframe["count"].to_dict()
            wc = WordCloud(width = 1920, height = 1080, background_color=color)
            wc.generate_from_frequencies(dict1)
            plt.figure(figsize=windowsize)
            plt.axis("off")
            plt.imshow(wc, interpolation="bilinear",aspect='auto')
            plt.show()
        elif type == "linked_accounts":
            bagframe = self.bagofwords(on='linked_accounts', extended_view=False, stopOWN = stopOWN)
            bagframe = bagframe.set_index('accounts')
            dict1 = bagframe["count"].to_dict()
            wc = WordCloud(width = 1920, height = 1080, background_color=color)
            wc.generate_from_frequencies(dict1)
            plt.figure(figsize=windowsize)
            plt.axis("off")
            plt.imshow(wc, interpolation="bilinear",aspect='auto')
            plt.show()
        else:
            raise TypeError('wordcloud: type not specified')

    def plot_hist(self, type, windowsize=(8,5),plotstyle = "ggplot", bins = 5, title = None, facecolor = 'blue', edgecolor = 'black', alpha = 0.8, font = 12):
        """
        Description
        -----------
        Plots histogram for likes and retweets.

        Parameters
        -----------
        type:                       type = str
                                    description = specify type of plot output
                                                  'likes' =     displays histogram of number of likes
                                                  'retweets' =  displays histogram of number of retweets

        windowsize:                 type = tuple
                                    description = sets figure size in inches.
                                    default = (8,5)

        plotstyle:                  type = matplotlib style sheet (str)
                                    default = "ggplot"

        bin:                        type = integer
                                    description = number of histogram bins
                                    default = 5

        facecolor:                  type = matplot lib color (str)
                                    decription = color of bars
                                    default = 'blue'

        edgecolor:                  type = matplot lib color (str)
                                    description = color of bin edges
                                    default = 'black'

        alpha:                      type = float
                                    description = opacity of bar facecolor
                                    default = 0.5

        font:                       type = int
                                    description = Setting the font size of the title, x label
                                    default = 12

        Returns
        -----------
        <none>

            --> diplays chart

        Examples
        -----------
        1.
            >>>> Parties = ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei","cdu","csu"]
            >>>> twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, Parties)
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = "2019-07-03", end_date = "2019-07-07")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.plot_hist(type="likes", bins = 10)
        """
        if type == 'likes':
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            n, bins, patches = plt.hist(self.df["likes"], bins, facecolor = facecolor, edgecolor = edgecolor, alpha = alpha)
            if title == None:
                plt.title('Histogram of Likes', fontsize = font)
            else:
                plt.title(title, fontsize = font)
            plt.xlabel('Likes', fontsize = font)
            plt.show()
        elif type == 'retweets':
            plt.style.use(plotstyle)
            plt.figure(figsize=windowsize)
            n, bins, patches = plt.hist(self.df["retweets"], bins, facecolor = facecolor, edgecolor = edgecolor, alpha = alpha)
            if title == None:
                plt.title('Histogram of Retweets', fontsize = font)
            else:
                plt.title(title, fontsize = font)
            plt.xlabel('Retweets', fontsize = font)
            plt.show()
        else:
            raise TypeError('plot_hist Error: type not specified')

    def plot_trend (self, type, timeframe = "daily", show_each_account = False, plotstyle = "ggplot", windowsize = (10,5), title = None, linewidth = 1, yticksize = 1.0, font = 12):
        """"
        Description
        -----------
        Plots trends (time series) by count of tweets, likes and retweets.

        Parameters
        -----------
        type:                       type = str
                                    description =  The column, one wants to obtain a trend plot from:
                                                   'count' =        displays tweet counts over time
                                                   'likes' =        displays likes over time
                                                   'retweets' =     displays retweets over time
                                    default =  'count'

        timeframe:                  type =  str
                                    description =  Setting the time frame of the time series one wants to plot (ONLY SUPPORTS DAILY FOR NOW).
                                                'daily' = Daily timeframe.
                                    default =  "daily"

        show_each_account:          type =  boolean
                                    description = If True: Shows a trendline for each account in the dataframe.
                                                  If False: Show one trendline (over all accounts).
                                    default = False

        plotstyle:                  type =  str
                                    description =  Setting the plot style.
                                    default =  "ggplot"

        windowsize:                 type =  tuple
                                    description = Setting the window size of the figure.
                                    default = (10, 5)

        linewidth:                  type =  boolean
                                    description =  Setting the linewidth.
                                    default =  1.0

        yticksize:                  type = float
                                    description = Setting the tick size on the y axis.
                                    default =  1.0

        font:                       type = int
                                    description = Setting the font size of the title, x and y label
                                    default = 12

        Returns
        -----------
        <none>

            --> diplays chart

        Examples
        -----------

        The following examples obtains Donald Trumps and Barack Obamas tweets and plots a trend of the number of tweets each day.

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.plot_trend(type="count")

        The following examples obtains Donald Trumps and Barack Obamas tweets and plots a trend of the number of tweets each day per account.

        2.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.plot_trend(type="count", show_each_account = True)

        The following examples obtains Donald Trumps and Barack Obamas tweets and plots a trend of the number of likes per tweet on each day per account.

        3.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump", "BarackObama"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
            >>>> tweet_analyzer = TweetAnalyzer(tweets)
            >>>> tweet_analyzer.plot_trend(type="likes", show_each_account = True, yticksize = 100.0)
        """
        register_matplotlib_converters()
        if timeframe == "daily":
            if show_each_account:
                df = self.df.copy()
                df["count"] = 1
                df = df[["author","likes","retweets", "date", "count"]]
                df.set_index(['author','date'], inplace = True)
                level_values = df.index.get_level_values
                df = df.groupby([level_values(0)]+[pd.Grouper(freq='D', level=-1)]).sum()
                mi = df.index.get_level_values(1).min()
                ma = df.index.get_level_values(1).max()
                r = pd.date_range(start=mi, end=ma)

                plt.style.use(plotstyle)
                fig, ax = plt.subplots(figsize = windowsize)

                if type == 'count':
                    for key, grp in df.groupby(level=0):
                        grp.reset_index(level=0, drop=True, inplace=True)
                        grp = grp.reindex(r, fill_value = 0)
                        ax.plot(grp.index, grp["count"], linewidth = 1.0, label=key)

                    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.yticks(np.arange(0, max(df["count"])+1, yticksize))
                    if title == None:
                        plt.title("Number of Tweets per Day", fontsize = font)
                    else:
                        plt.title(title)
                    plt.ylabel("Frequency", fontsize = font)
                    plt.xlabel("Date", fontsize = font)
                    plt.legend()
                    plt.show()
                elif type == 'likes':
                    for key, grp in df.groupby(level=0):
                        grp.reset_index(level=0, drop=True, inplace=True)
                        grp = grp.reindex(r, fill_value = 0)
                        ax.plot(grp.index, grp["likes"], linewidth = 1.0, label=key)

                    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.yticks(np.arange(0, max(df["likes"])+1, yticksize))
                    if title == None:
                        plt.title("Number of Likes per Day", fontsize = font)
                    else:
                        plt.title(title)
                    plt.ylabel("Frequency", fontsize = font)
                    plt.xlabel("Date", fontsize = font)
                    plt.legend()
                    plt.show()
                elif type == 'retweets':
                    for key, grp in df.groupby(level=0):
                        grp.reset_index(level=0, drop=True, inplace=True)
                        grp = grp.reindex(r, fill_value = 0)
                        ax.plot(grp.index, grp["retweets"], linewidth = 1.0, label=key)

                    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.yticks(np.arange(0, max(df["retweets"])+1, yticksize))
                    if title == None:
                        plt.title("Number of Retweets per Day", fontsize = font)
                    else:
                        plt.title(title)
                    plt.ylabel("Frequency", fontsize = font)
                    plt.xlabel("Date", fontsize = font)
                    plt.legend()
                    plt.show()
                else:
                    raise TypeError('tweet_plotter Error: plot_daily type not specified')

            else:
                df = self.df.copy()
                df.set_index('date', inplace=True)
                df["count"] = 1
                df = df[["likes","retweets", "count"]]
                df = df.resample('D').sum()

                plt.style.use(plotstyle)
                fig, ax = plt.subplots(figsize = windowsize)

                if type == 'count':
                    ax.plot(df.index, df["count"], linewidth = 1.0)
                    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.yticks(np.arange(min(df["count"]), max(df["count"])+1, yticksize))
                    if title == None:
                        plt.title("Number of Tweets per Day", fontsize = font)
                    else:
                        plt.title(title)
                    plt.ylabel("Frequency", fontsize = font)
                    plt.xlabel("Date", fontsize = font)
                    plt.show()
                elif type == 'likes':
                    ax.plot(df.index, df["likes"], linewidth = 1.0)
                    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.yticks(np.arange(min(df["likes"]), max(df["likes"])+1, yticksize))
                    if title == None:
                        plt.title("Number of Likes per Day", fontsize = font)
                    else:
                        plt.title(title)
                    plt.ylabel("Frequency", fontsize = font)
                    plt.xlabel("Date", fontsize = font)
                    plt.show()
                elif type == 'retweets':
                    ax.plot(df.index, df["retweets"], linewidth = 1.0)
                    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                    plt.yticks(np.arange(min(df["retweets"]), max(df["retweets"])+1, yticksize))
                    if title == None:
                        plt.title("Number of Retweets per Day", fontsize = font)
                    else:
                        plt.title(title)
                    plt.ylabel("Frequency", fontsize = font)
                    plt.xlabel("Date", fontsize = font)
                    plt.show()
                else:
                    raise TypeError('tweet_plotter Error: plot_daily type not specified')

class UserAnalyzer:
    """
    Description
    -----------
    Functionality for analyzing and categorizing content from tweets.
    It is of course based on the TwitterClient(), which returns the "raw" data.
    """
    def __init__(self, users = None, df = None):
        """
        Description
        -----------
        This class can be initialized via the data fetched by TwitterClient().get_user_data(): The raw tweet data.
        If no dataframe is provided, it will automaticly create a dataframe including metadata (see function: users_to_dataframe)

        IMPORTANT:
        If you create a UserAnalyzer object by passing a custom dataframe:
        Make sure it has the same structure (Column Names/Data Types) as the one created by the class function: users_to_dataframe!

        If you don't provide any tweets and no Dataframe: FUNCTIONS will obviously not work!
        --> You can load a csv as a dataframe and work with it (see function write_to_csv)

        Parameters
        ----------
        users:              type = <class 'list'>
                            description =  A list created by the TwitterClient Class which is using tweepy package to obtain the raw user data via the twitter API
                            default = None

        df:                 type = <class 'pandas.core.frame.DataFrame'>
                            description = Dataframe, which includes several meta data on every user
                            default = None

        Returns
        -------
        <class 'tweet_analyzer.TweetAnalyzer'>

            --> By calling, it instantiates a UserAnalyzer Object

        Example(s)
        ----------
        The following examples instantiates a UserAnalyzer with the account of Donald Trump.

        1.
            >>>> consumer_key = "Example_xyz1"
            >>>> consumer_secret = "Example_xyz2"
            >>>> access_token = "Example_xyz3"
            >>>> access_token_secret = "Example_xyz4"
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> users = twitter_client.get_user_data()
            >>>> user_analyzer = UserAnalyzer(users)
        """
        if users == None:
            self.users = users
            self.df = df

        else:
            self.users = users
            self.df = df if df is not None else self.users_to_dataframe(self.users)

    def users_to_dataframe(self,users):
        """
        Description
        -----------
        This function creates a dataframe of the TwitterClient().get_user_data() returned user_data:
        By obtaining serveral informations of the user object, stored in separate columns, we get:
        * The account ("author of the tweet")
        * The follower count of each account
        * The date (when the account was created)

        Parameters
        ----------
        tweets:             type = <class 'list'>
                            description = A list created by the TwitterClient Class which is using tweepy package to obtain the raw user data via the twitter API

        Returns
        -------
        <class 'pandas.core.frame.DataFrame'>

            --> A dataframe is returned, which includes several meta data on every tweet

        Example(s)
        ----------
        The following examples obtains Donald Trumps user data and creating a dataframe:

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_data()
            >>>> df = UserAnalyzer().users_to_dataframe(users)
        """
        L = []
        for user in users:
            L.append([user.screen_name,
                        user.followers_count,
                        user.created_at])
        return (pd.DataFrame(L, columns = ["author", "account_followers", "account_created"]))

    def get_dataframe(self):
        """
        Description
        -----------
        This function returns the meta-dataframe of this class.

        Parameters
        ----------
        No parameters are passed.

        Returns
        -------
        <class 'pandas.core.frame.DataFrame'>

            --> A dataframe is returned, which includes several meta data on every tweet

        Example(s)
        ----------
        The following examples obtains Donald Trumps user data and returns the dataframe:

        1.
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_data()
            >>>> user_analyzer = TweetAnalyzer(users)
            >>>> tweet_analyzer.get_dataframe()
        """
        return self.df

    def write_to_csv(self, *args, **kwargs):
        """
        Description
        -----------
        Write dataframe to a comma-separated values (csv) file.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
        """
        self.df.to_csv(*args, **kwargs)

    def read_from_csv(self, *args, **kwargs):
        """
        Description
        -----------
        Read a comma-separated values (csv) file into a dataframe.

        --> Uses the corresponding pandas function. Documentation can be found at:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        """
        self.df = pd.read_csv(*args, **kwargs)
        self.df.account_created = pd.to_datetime(self.df.account_created)

    def plot_bar_follower(self, facecolor = "blue", edgecolor = "blue", alpha = 0.5, title = None, plotstyle = "ggplot",
                        xvalues = False, sort_val = True, windowsize = (10,5), colordict = None, font = 12):
        """
        Description
        -----------
        Plots a bar chart of the follower count.

        Parameters
        -----------
        windowsize:                 type = tuple
                                    description = sets windowsize in inches
                                    default = (10,5)

        plotstyle:                  type = matplotlib style sheet (str)
                                    default = "ggplot"

        title:                      type = str
                                    description = plot title
                                    default = 'Top x most used words'

        xvalues:                    type = boolean
                                    description = True to show values for the bars
                                    default = False

        facecolor:                  type = matplotlib color (str)
                                    description = color of bars
                                    default = 'blue'

        edgecolor:                  type = matplotlib color (str)
                                    description = color of bar edges
                                    default = 'blue'

        alpha:                      type = float
                                    description = sets opacity of the color bars
                                    default = 0.5

        sort_val:                   type = boolean
                                    description = sort values in bar graph
                                    default = True

        colordict:                  type = dict
                                    description = Specify a dictionary with the xlabels as keys and the color as values. The xlabels will be colored accordingly
                                    default = None

        Returns
        -----------
        <none>

            --> diplays chart

        Examples
        -----------
        1.
            >>>> Parties = ["spdde", "fdp","die_Gruenen","afd","dieLinke","fwlandtag","diepartei","cdu","csu"]
            >>>> twitter_client = TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, Parties)
            >>>> tweets = twitter_client.get_user_data()
            >>>> user_analyzer = UserAnalyzer(tweets)
            >>>> colordict = {'fwlandtag':"green", "CSU":"red", "fdp":"green", "Die_Gruenen":"green", "spdde":"red", "dieLinke":"red", "CDU":"red", "DiePARTEI":"green", "AfD":"green"}
            >>>> user_analyzer.plot_bar_follower(sort_val = True, xvalues = True, colordict = colordict)
        """
        df = self.df.copy()
        if sort_val:
            df.sort_values(by=["account_followers"], inplace = True)
        plt.style.use(plotstyle)
        fig, ax = plt.subplots(figsize = windowsize)
        rects = plt.barh(df.author, df.account_followers, color = facecolor, edgecolor = edgecolor, alpha = alpha)
        ax.set_yticklabels(df.author)
        if colordict != None:
            for ytick in ax.get_yticklabels():
                ytick.set_color("white")
                for key, value in colordict.items():
                    if ytick.get_text()==key:
                        bbox = dict(boxstyle="round", ec=value, fc=value, alpha=1)
                        plt.setp(ytick, bbox=bbox)
        if xvalues:
            c = 0
            for rect in rects:
                plt.text(s=str(rect.get_width()),x=rect.get_width()+0.5,y=c,color='black',verticalalignment="center",horizontalalignment="left",size = 10)
                c += 1
        if title == None:
            plt.title('Users Follower Count', fontsize = font)
        else:
            plt.title(title, fontsize = font)
        plt.xlabel('Count', fontsize = font)
        plt.ylabel('Accounts', fontsize=font)
        plt.show()
