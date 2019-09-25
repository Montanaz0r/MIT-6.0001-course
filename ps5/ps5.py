import feedparser
import time
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import string


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger object.
        Phrase(string) is one or more words separated by a single space
        between the words. Phrase does not contain any punctuation.
        Examples:
            are phrases:
            ● 'purple cow'
            ● 'PURPLE COW'
            ● 'mOoOoOoO'
            ● 'this is a phrase'
            are not valid phrases:
            ● 'purple cow???' ​ (contains punctuation)
            ● 'purple cow' ​ (contains multiple spaces between words)
            '''
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        ''' this method takes one argument - text(string),
        and returns True if the whole phrase is present in the text,
        False otherwise. Method should trigger as presented in the examples
        below, given that the phrase is "purple cow".
        Should trigger:
        ● 'PURPLE COW'
        ● 'The purple cow is soft and cuddly.'
        ● 'The farmer owns a really PURPLE cow.'
        ● 'Purple!!! Cow!!!'
        ● 'purple@#$%cow'
        ● 'Did you see a purple cow?'
        Should NOT trigger:
        ● 'Purple cows are cool!'
        ● 'The purple blob over there is a cow.'
        ● 'How now brown cow.'
        ● 'Cow!!! Purple!!!'
        ● 'purplecowpurplecowpurplecow'
        '''
        word_separators = string.punctuation   # Assigns all possibles separators to a variable.
        phrase_list = self.phrase.split(' ')   # Making a list for our phrase to allow comparision later on.
        text = text.lower()   # Method is not case sensitive!
        success_validation = False
        for separator in word_separators:   # Each possible separator will be replaced in the text by space.
            if separator in text:
                text = text.replace(separator, ' ')
        text_list = text.split()   # To allow comparision we will create a list of text splitting all spaces.
        for index in range(len(text_list)):
            if success_validation is True:
                break
            if text_list[index] == phrase_list[0]:
                for i in range(len(phrase_list)):
                    try:
                        if text_list[index + i] != phrase_list[i]:
                            success_validation = False
                            break
                        else:
                            success_validation = True
                    except IndexError:
                        success_validation = False
        return success_validation

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time_str):
        '''
        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
        Convert time from string to a datetime before saving it as an attribute.
        '''
        self.time = datetime.strptime(time_str, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))


# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_str):
        super().__init__(time_str)

    def evaluate(self, story):
        return self.time > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


class AfterTrigger(TimeTrigger):
    def __init__(self, time_str):
        super().__init__(time_str)

    def evaluate(self, story):
        return self.time < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        return self.first_trigger.evaluate(story) and self.second_trigger.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        return self.first_trigger.evaluate(story) or self.second_trigger.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
    return triggered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    names_dict = {'TITLE': TitleTrigger, 'DESCRIPTION': DescriptionTrigger,   # Dictionary that maps each key word from
                  'BEFORE': BeforeTrigger, 'AFTER': AfterTrigger,   # triggers to actual name of trigger.
                  'NOT': NotTrigger, 'AND': AndTrigger,
                  'OR': OrTrigger}
    triggers_dict = {}   # Each line from triggers.txt is saved as dictionary, where key=name, values=trigger,args.
    triggers_list = []   # Triggers list will be filled in only with triggers that user decided to run (ADD statement).
    for line in lines:
        line = line.split(',')
        if line[1] in ['TITLE', 'DESCRIPTION', 'BEFORE', 'AFTER']:
            triggers_dict[line[0]] = names_dict[line[1]](line[2])
        elif line[1] == 'NOT':
            triggers_dict[line[0]] = names_dict[line[1]](triggers_dict[line[2]])
        elif line[1] in ['AND', 'OR']:
            triggers_dict[line[0]] = names_dict[line[1]](triggers_dict[line[2]], triggers_dict[line[3]])
        elif line[0] == 'ADD':
            for index in range(1, len(line)):
                triggers_list.append(triggers_dict[line[index]])
    print(triggers_list)
    return triggers_list

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("Trump")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Warren")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1]

        # Problem 11

        triggerlist = read_trigger_config('triggers.txt')
        print(triggerlist)
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

