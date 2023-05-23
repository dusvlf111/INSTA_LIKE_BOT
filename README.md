# **Insta Like Automation**

> # Instagram prohibits crawling.<br> Even if you get caught and suffer damage<br> I do not take any responsibility.


## program description

  This is a program that searches with the desired tag and clicks likes as many times as the number of likes.<br><br>
In the case of a program that likes my postings, when I pay for an Instagram ad, the person who likes or follows me is advertised first, which reduces the advertising efficiency.<br><br>
However, I think it is an efficient program because you can expect advertising effects and follow by pressing likes on related tags. <br><br>
`If you do not understand the code, please email me personally and I will respond`

## Note

- In order not to be caught as a bot, the user-agent is set arbitrarily, but you need to change it to suit the user.
- This program was made to move in replit, but if it does not move, it can be used by modifying the setup_driver. <br> (Modify on your own according to the usage environment a)
- It was produced with the goal of making a program, and while it was made, it was also distributed as a package. The role of package may not be enough.
- Display the progress in log and save it as a file. When the program is re-executed, the previous log file is deleted.<br> (Delete log class inheritance if unnecessary)

### link

[link text] (link URL)

### image

![image alt text] (image URL)

## Code Class structure


  - Insta_Like (Logger):
      - Inherits from the Logger class.
      - Override the `__new__` method so that only one instance of the class is created.
      - Override the `__init__` method to set up an instance with your Instagram account ID and password.
      - Define several ways to automate the like process.
          - `setup_driver`: Sets and returns a Chrome webdriver instance with specific options.
          - `go_site`: Go to the Instagram homepage.
          - `Login`: Log in to your Instagram account with the provided ID and password.
          - `go_tag`: Go to Instagram's tag page.
          - `send_like`: Like a certain number of posts on the tag page.
           




## Basic code example

```python

     #Create class instance
     insta = Insta_Like('Insert your Insta ID', 'Your Insta password')
     #go to site
     insta.go_site()
     #log in
     insta.Login()

     # go to tag
     insta.go_tag('Insert the tag you want to add!!')

     #Set the number of likes
     insta.send_like('Number of likes to click here', True)

     # Struggle to not get caught by Instabot
     time.sleep(random.uniform(5.0, 10.0))

     # Close webdriver
     insta. done()

```

## Usage examples
```python

    #Create class instance
    insta = Insta_Like('Insta ID', 'Password')
    #go to site
    insta.go_site()
    #log in
    insta.Login()
     
    # Tag List Randomly selected tags are inserted
    tag_list = [
        'instagood', 'photooftheday', 'beautiful', 'love',
        'fashion', 'happy', 'cute', 'like4like', 'followme',
        'picoftheday', 'art', 'photography', 'style', 'nature',
        'fun', 'travel', 'smile', 'food', 'model', 'follow4follow',
        'music', 'beauty', 'summer', 'igers', 'likeforlike', 'fit',
        'motivation', 'blogger', 'quote', 'dog'
    ]

    # When you press Like once (put in to measure the time while running)
    start_time = time.monotonic()
    
    while True:
        # Choose an integer between 3 and 10
        send_like_num = random.randint(3,10)
        #randomly select from list
        tag_select = random.choice(tag_list)
        # go to tag
        insta.go_tag(tag_select)
        
        try:
            # I handled the exception, but I was afraid it would break...
            insta.send_like(send_like_num,True)
        
        except:
            # Set to move to the next tag when an exception occurs without liking
            print(f'There was an error in tag {tag_select}. Skip it')
            continue
            
        time.sleep(random.uniform(5.0, 10.0))
        
        end_time = time. monotonic()
        elapsed_time = time.timedelta(seconds= end_time - start_time)
         
        # Measure tag execution time
        print(
            f"Tag name: {tag_select} \n",
            f"Execution time: {elapsed_time} \n",
            f"Number of likes: {send_like_num}",
        )
        
```
