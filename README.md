# staqutech
A Twitter bot for scraping data related to given twitter handle.
This project is part of backend intern challenge @ www.staqu.com

## Project Configuration
Specify your Consumer key,secret and Access key,secret in **configuration.py** file residing in staqu_bot/script/ folder

## Usages
Execute the **bot_cli.py** file with following commands - 
* **-h** or **--handler** : To specify the twitter handler/scren_name (mandatory), exapmle
```python
>>> python bot_cli.py -h staqutech
```
* **-f** or **--follower** : Flag specify downloading of follower data, example
```python
>>> python bot_cli.py -h staqutech -f
```
* **-t** or **--tweet** : Flag specify downloading of tweet data, example
```python
>>> python bot_cli.py staqutech -t
```
* **--help** : Open the help menu
* Both follower and tweet data can be downloaded simultaneously, example
```python
>>> python bot_cli.py -h staqutech -f -t
```
* Specifying one flag is mandatory

## Notes
1. Downloaded data will be saved in dynamically generated folder residing in staqu_bot/data/
2. File naming convention - **[handle_name]\_[data type].tsv** , Example _staqutech_follower.tsv_ or _staqutech_tweet.tsv_
3. Files are opened in **a+** mode, so new data will be appended in existing file with same name
