import praw
import time
from bs4 import BeautifulSoup
import requests
import re

def run_bot(reddit):
    
    sub = reddit.subreddit("umanitoba").new(limit = 20)   #get the latest posts on the subreddit

    for post in sub: #looping through all the latest posts 
        if ("!find" in post.selftext) and (not post.saved):  # checking if the bot is called in that post and if the bot hasn't already replied 
            reply_post(post)

        post.comments.replace_more(limit=None)
        for comment in post.comments.list(): #looping through all the comments (even replies to other comments)
            if ("!find" in comment.body) and (not comment.saved):
                reply_comment(comment)

            
# not using sub.stream.comments() or sub.stream.submissions() as that will be much more complicated to check for both new comments and posts continuously
# so it is best to do it manually and have the bot run once every certain minutes as the subreddit itself isn't very active


def reply_comment(comment):
    bot_request = comment.body.upper().split("!FIND", 2)[1].strip()  #get only the 2 words after !find which represent the course name & code
    request = bot_request.split(" ")  #separate the course name and code 
    course_name = request[0].strip() 
    course_code = request[1].strip()
    bot_reply = get_info(course_name, course_code)
    comment.reply(bot_reply + "\n\n**BEEP BOP. I'm a bot. You can contact my creator [here](https://www.reddit.com/message/compose?to=CanadianSorryPanda&subject=&message=)**")
    comment.save()  # save the comment so the bot doesn't reply to it multiple times
    print("Replied to a comment")
    
def reply_post(post):
    bot_request = post.selftext.upper().split("!FIND", 2)[1].strip()
    request = bot_request.split(" ")
    course_name = request[0].strip()
    course_code = request[1].strip()
    bot_reply = get_info(course_name, course_code)
    post.reply(bot_reply + "\n\n**BEEP BOP. I'm a bot. You can contact my creator [here](https://www.reddit.com/message/compose?to=CanadianSorryPanda&subject=&message=)**")
    post.save()
    print("Replied to a post")
  
  
def login_bot(): 
    
    reddit = praw.Reddit(client_id = "",  
                         client_secret = "",
                         password = "",
                         user_agent = "",
                         username = "")
    return reddit


def get_info(course_name, course_code):
    term = ''

    date_today = time.localtime()
    date_today_year = str(date_today.tm_year)
    date_today_month = date_today.tm_mon

    # determine the term that we are in, this will query aurora for the current term
    if date_today_month >= 9:
        term = date_today_year + '90'
    elif date_today_month >= 5:
        term = date_today_year + '50'
    else:
        term = date_today_year + '10'

    url = 'https://aurora.umanitoba.ca/banprod/bwckctlg.p_disp_course_detail?cat_term_in={}&subj_code_in={}&crse_numb_in={}'.format(term, course_name, course_code)
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    title = soup.find("td", class_ = "nttitle")
    
    if not title: # if empty, this means the course name doesn't exist 
        return "Sorry, I couldn't find the course you were looking for :("
        
    # find the description of the course and strip it of all the newlines
    desc = soup.find("td", class_ = "ntdefault").text.replace('\n', '')
    # get only the part upto where it says "Credit hours"
    desc = re.findall('(.*) Credit hours', desc)[0]
    # split on '.-', first element will be description and second part will be cr hours
    split_desc = desc.split('.-')

    # find the faculty this course belongs to
    fac = soup.find('a', href = re.compile('/banprod/bwckctlg\.p_disp_listcrse')).text

    name = "*Course name:* " + title.text.strip()
    faculty = "*Faculty:* " + fac.strip()
    credit_hours = "*Credit hours:* " + split_desc[1].strip()
    description  = "*Description:* " + split_desc[0].strip()
        
    return (name + "\n\n" + faculty + "\n\n" + credit_hours + "\n\n" + description)
    

def main():  
    
    reddit = login_bot()
    
    while True: 
        try:
            run_bot(reddit)
            print("Sleeping")
            time.sleep(120) # bot checks for new posts or comments once every 2 minutes
        except praw.exceptions.PRAWException as e:
            print("PRAW error: " + str(e))
            print("Waiting")
            time.sleep(600) # rest for 10 minutes if PRAW related error, longer wait-time is fine as the subreddit is not very active
        except Exception as e:
            print("Error: " + str(e))
            break  
        # if a non-PRAW error occurs then stop the program, if you want to run the bot indefinitely simply replace this line with time.sleep()
    


if __name__ == "__main__": # for Python interpreter if you want to run the bot from there as a py file
    main()
  
    
main()
    
    
