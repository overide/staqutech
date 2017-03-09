# Script for fancy command line like interface

import os
import threading
import sys
from bot import *

NUMBER_OF_THREADS = 2


def sys_args_handler(args):
    '''
    handle the command line arguments and perform actions
    '''
    if not len(args):
        print("""bot_cli: missing arguments
	Try 'bot_cli --help' for more information.""")
        sys.exit()
    elif len(args) == 1 and args[0] == '--help':
        print("""Download the twitter data of the entered handle
Usages : bot_cli [option] [argument] [flag] \n
Mandatory arguments to long options are mandatory for short options too.
\t -h,  --handle\t Set handle of the user
\t -f,  --follower Flag to download follower data
\t -t,  --tweet\t Flag to download tweet data 
\t      --help\t Display the help and exit""")
        sys.exit()
    else:
        possible_cmds = ['-h', '--handle', '-f',
                         '--follower', '-t', '--tweet', '--help']
        handle = None
        dl_follow = False
        dl_tweet = False

        if '-h' not in args and '--handle' not in args:
            print("""Providing a handle is mandatory
Try 'bot_cli --help' for more information.""")
            sys.exit()

        for i, cmd in enumerate(args):
            try:
                if cmd == '-h' or cmd == '--handle':
                    if args[i + 1] not in possible_cmds:
                        handle = args[i + 1]
                        del args[i + 1]
                elif cmd == '-f' or cmd == '--follower':
                    dl_follow = True

                elif cmd == '-t' or cmd == '--tweet':
                    dl_tweet = True

                else:
                    print("""bot_cli: invalid arguments {}
Try 'bot_cli --help' for more information.""".format(cmd))
                    sys.exit()
            except IndexError:
                print("""bot_cli: missing arguments
Try 'bot_cli --help' for more information.""")

        if handle and not (dl_follow or dl_tweet):
            print("""bot_cli: missing arguments, provide -f or -t flag.
Try 'bot_cli --help' for more information.""")
            sys.exit()
        else:
            return handle, dl_follow, dl_tweet


def validate_handle(api, handle):
    '''
    Validated given handle, whether it exists or not
    if not exist, exit script
    '''
    try:
        api.get_user(screen_name=handle)
        return True
    except tweepy.TweepError:
        print("Handle @{} do not exist!".format(handle))
        sys.exit()


def start_jobs(handle, dl_follow, dl_tweet, api):
    '''
    Create threads and execute them
    Arguments-
            handle 		: Twitter screen name
            dl_follow 	: Boolean field, specify whether to download follower
                          data or not
            dl_tweet 	: Boolean field, specify whether to download follower
                          data or not
            api 		: API instance
    '''

    if dl_follow:
        t1 = threading.Thread(target=get_followers, args=(api, handle,))
        t1.daemon = True
        t1.start()

    if dl_tweet:
        t2 = threading.Thread(target=get_tweets, args=(api, handle,))
        t2.daemon = True
        t2.start()

    if dl_follow and dl_tweet:
        t1.join()
        t2.join()
    else:
        t1.join() if dl_follow else t2.join()


def main():
    auth = initialize_auth()
    api = tweepy.API(auth)
    handle, dl_follow, dl_tweet = sys_args_handler(sys.argv[1:])
    if validate_handle(api, handle):
        start_jobs(handle, dl_follow, dl_tweet, api)

if __name__ == '__main__':

    if not os.path.exists('../data'):
        os.makedirs('../data')
    main()