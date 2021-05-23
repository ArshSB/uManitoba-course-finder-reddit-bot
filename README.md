# course-finder-reddit-bot
a uManitoba subreddit version of my previous course finder bot

See the bot in action [here](https://www.reddit.com/user/kidshelplinebot)

## Purpose
this bot monitors the uManitoba subreddit and replies to users with their requested course description and prerequisites from the uManitoba database.

Please note the database is not readily available in one place and webpage so I used [this](http://crscalprod.ad.umanitoba.ca/Catalog/ViewCatalog.aspx?pageid=viewcatalog&topicgroupid=27309&entitytype=CID&entitycode=COMP+1010) arbitrary link and manipulated the URL content by replacing the last part of the link with a specific course name and code, which yields a new webpage with the respective course information

Note: As of May 2021, uManitoba has updated their databases and their website, so the above link is invalid. Perhaps in the near future I will update the code to fix this change.

## Usage
either through commenting or posting in the subreddit, simply call the bot like this
```
!find *course_name* *course_code*
```
make sure to leave a space between *!find, course_name and course_code*

## Getting started
1. [register](https://ssl.reddit.com/prefs/apps/) an app with Reddit for authenticatication. Instructions [here](https://praw.readthedocs.io/en/latest/getting_started/authentication.html)
2. input your **client information, username and password** in *login_bot()* 
3. if desired, change or remove how often the bot checks for new posts and comments in *main()* 
4. run *main()* or the py file in the interpreter to start the bot!

## Built With
* [Python 3.8.3](https://www.python.org/downloads/)
* [PRAW 7.0.1](https://praw.readthedocs.io/en/latest/index.html) - for working with Reddit API
* [BeautifulSoup 4.9.0](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - for course database parsing
