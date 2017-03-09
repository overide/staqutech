#!/usr/bin/env python
# encoding: utf-8
# contain core processing methods 

import tweepy
import csv
import time
import credentials
FILE_PATH = "../data/"


def initialize_auth():
    '''
    Authenticate user to the Twitter app
    Return an OAuth Object
    '''
    auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY,
                               credentials.CONSUMER_SECRET)
    auth.set_access_token(credentials.ACCESS_KEY, credentials.ACCESS_SECRET)
    return auth

def write_to_file(data, file_name, initial=True, write_for="tweet"):
    '''
    Write data to the file
    Arguments-
        data            : a list of data
        file_name       : name of file to be created
        initial         : Boolean value indicating whether it's first call to this method
        write_for       : indicate whether write tweet or follower data, possible values 
                    are "tweet" and "follower"
    '''
    with open(FILE_PATH + file_name + ".tsv", "a+") as fh:
        writer = csv.writer(fh, delimiter="\t")
        if initial:
            if write_for == 'tweet':
                writer.writerow(['id', 'created_at', 'text'])
            elif write_for == 'follower':
                writer.writerow(['id', 'screen_name', 'name'])
            else:
                raise ValueError("""Argument 'write_for' received illegal value, must
                                 be 'tweet' or 'follower'.""")
        for row in data:
            writer.writerow(row)


def prepare_data(data, prepare_for='tweet'):
    '''
    Prepare data for being written in file
    Arguments -
        data           : data to be prepared
        prepare_for    : specify whether prepare tweet or follower data
    '''
    if prepare_for == 'tweet':
        return [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")]
                 for tweet in data]
    elif prepare_for == 'follower':
        return [[follower.id_str, follower.screen_name, follower.name]
                 for follower in data]
    else:
        raise ValueError("""Argument 'prepare_for' received illegal value,
                         must be 'tweet' or 'follower'.""")


def fetch_data(cursor, filename, fetch_for="tweet"):
    '''
    Fetch data through API

    If ratelimit exceeds:
        -it dump fetched data to the file and pause for 17 minutes
        -clear the old fetched data

    Arguments -
        cursor      : A cursor instance
        filename    : name of the file
        fetch_for   : Specify what data to fetch, tweet or follower
    '''
    fetched_data = []
    initial = True
    while True:
        try:
            fetched_data.append(cursor.next())

        except tweepy.RateLimitError:
            print("Rate Limit exceeded, wait for 16 minutes...")
            print("Writing existing data to the file "+filename+"...")

            # dump existing data to the file
            fetched_data = prepare_data(fetched_data, fetch_for)
            write_to_file(fetched_data, filename, initial, fetch_for)
            if initial:
                initial = False

            # clear the list
            fetched_data.clear() 
            time.sleep(16 * 60)
            print("Resuming...")

        except tweepy.TweepError:
            print("Oh snap!, some error occured, retrying in 1 minute...")
            time.sleep(60)
            print("Resuming...")

        except StopIteration:
            break

    fetched_data = prepare_data(fetched_data,fetch_for)
    write_to_file(fetched_data,filename,initial,fetch_for)

def get_followers_count(api, handle):
    '''
    Return the count of number of follower of handle
    Arguments - 
        api     : API instance 
        handle  : screen name of twitter user
    '''
    try:
        return len(api.followers_ids(screen_name=handle))
    except tweepy.RateLimitError:
        time.sleep(16 * 60)
        return get_followers_count(api, handle)

def get_followers(api,handle):
    '''
    Download the list of all the followers for the given handle
    Arguments - 
        api     : API instance 
        handle  : screen name of twitter user
    '''
    print("Downloading follower data for handle @"+handle)
    followers_cursor = tweepy.Cursor(api.followers, screen_name=handle, count=200).items()
    fetch_data(followers_cursor,handle+"_followers","follower")

    # write the total follower count to the file
    follower_count = [["Total Followers: ",get_followers_count(api, handle)]]
    write_to_file(follower_count,handle+"_followers",False,"follower")

    print("Successfully fetched all followers!")

def get_tweets(api, handle):
    '''
    Download only 3200 historical tweets of the given handle
    Twitter allow access to only 3200 tweets through their API, that's their policy
    Other options : Using paid Gnip service to get access to API for historical tweets  
    Arguments - 
        api     : API instance 
        handle  : screen name of twitter user
    '''
    print("Downloading tweet data for handle @"+handle)
    tweet_cursor = tweepy.Cursor(api.user_timeline, screen_name=handle, count=200).items()
    fetch_data(tweet_cursor,handle+"_tweets","tweet")
    print("Successfully fetched all tweets!")   