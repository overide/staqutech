# staqutech
A Twitter bot for scraping data related to given twitter handle.
This project is a part of backend intern challenge @ www.staqu.com

## Project Configuration
Specify your consumer key,secret and access key,secret in **configuration.py** file residing at **staqu_bot/scripts/** folder

## Usages
Execute the **bot_cli.py** file with following commands - 
* **-h** or **--handle** : To specify the twitter handler/screen_name (mandatory), example
```python
>>> python bot_cli.py -h staqutech
```
* **-f** or **--follower** : Flag specify downloading the follower data, example
```python
>>> python bot_cli.py -h staqutech -f
```
* **-t** or **--tweet** : Flag specify downloading the tweet data, example
```python
>>> python bot_cli.py -h staqutech -t
```
* **--help** : Open the help menu
* Both follower and tweet data can be downloaded simultaneously, example
```python
>>> python bot_cli.py -h staqutech -f -t
```
* Specifying one flag is mandatory

## Notes
1. Downloaded data will be saved in dynamically generated folder residing at **staqu_bot/data/**
2. File naming convention - **[handle]\_[data].tsv** , Example _staqutech_followers.tsv_ , _staqutech_tweets.tsv_
3. Files are opened in **a+** mode, so new data will be appended in existing file with same name
