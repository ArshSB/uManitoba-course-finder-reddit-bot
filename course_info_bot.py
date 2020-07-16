import praw
import time
from bs4 import BeautifulSoup
import requests

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
    
    url = "http://crscalprod.ad.umanitoba.ca/Catalog/ViewCatalog.aspx?pageid=viewcatalog&topicgroupid=27309&entitytype=CID&entitycode=" + course_name + "+" + course_code  #get the database for the course name
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    text_td = soup.find_all("td", class_ = "courseValueCell")  # get course information from the webpage and save the name, decription etc. as a list
    
    if not text_td: # if empty, this means the course name doesn't exist 
        return "Sorry, I couldn't find the course you were looking for :("
    
    else:
        name = "*Course name:* " + text_td[2].text    
        faculty = "*Faculty:* " + text_td[4].text
        credit_hours = "*Credit hours:* " + text_td[1].text
        description  = "*Description:* " + text_td[3].text
        
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
    
    
