from bs4 import BeautifulSoup as bs4
import pandas as pd
import requests
from flair.models import TextClassifier
from flair.data import Sentence
import statistics
import re
import time
import numpy as np
from project_plotting import * # custom plot functions
classifier = TextClassifier.load('en-sentiment')

html= requests.get("https://www.imdb.com/chart/top/").text #text body from imdb 

soup = bs4(html, 'html.parser') # creating soup parsing object

movies = soup.select('td.titleColumn') # selecting title from soup
ratings = [b.attrs.get('data-value')
           for b in soup.select('td.posterColumn span[name=ir]')] # selecting rating from imdb

# cleaning data and getting title,year,rating for movies
all_info = []
for index in range(0, len(movies)):

    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    data = {"movie_title": movie_title,
            "year": year,
            "rating": ratings[index]}
    all_info.append(data)
    
#converting it to dataframe
df = pd.DataFrame(all_info)

# apppending all unique id of review_url, and getting genres
all_id = []
all_titles = []
all_reviews = []
genres = []

u_id = re.findall('/title/(tt[0-9]+?)/', html)

review = 'https://www.imdb.com/title/{}/reviews'
title = 'https://www.imdb.com/title/{}'

#appending unique id for all movies
for i in u_id:
    if i not in all_id:
        all_id.append(i)
        
#appending reviews url       
for i in all_id:
    reviews = review.format(i)
    all_reviews.append(reviews)
    
# appending movies url
for i in all_id:
    titles = title.format(i)
    all_titles.append(titles) 
    
## appending genres     
for a in all_titles:
    one_review = requests.get(a).text
    genre= re.search(r"\"genre\":(\[.*?\])"," ".join(one_review.split("\n")),re.DOTALL)
    if genre:
        genres.append(sorted([kk.strip('"') for kk in genre[1][1:-1].split(",")]))
    else:
        genres.append([])
        
df['reviews_url'] = all_reviews
df['genres'] = genres

#looping through all genres and append '1' if not in the list
all_gs=[]
for g in genres:
    for l in g:
        if l not in all_gs:
            all_gs.append(l)
all_gs=sorted(all_gs)

for j in all_gs:
    df[j] = None
    
count=0
gens={}
rowvalues=[]

# iterating through all genres and counting and appending with 1 and 0
for i in df.iterrows():
    listthem = df.iloc[count]["genres"]
    print(listthem)
    listit=[]
    for h in all_gs:
        print(h)
        if h in listthem:
            listit.append(1)
        else:
            listit.append(0)
    rowvalues.append(listit)
    count+=1
    
rowvalues
# creating an array with 1 and 0 for genres
dfn=np.array(rowvalues)
transpoz=dfn.T # transposing the array
transpoz=transpoz.tolist() # converting to list
for j in range(0,len(all_gs)):
    df[all_gs[j]]=transpoz[j] # creating columns in df for genres and storing 1 and 0

from selenium.webdriver import Firefox  # importing library for webfriver of selenium

browser = Firefox() #initiating the browser



## Itertaing through review url to grab all the reviews text from each movies approximately 30 - 75 reviews. <br><br>
##Using selenium for load more to find and click it. <br><br>
##Counter to load maximum of 3 times to get all reviews from each movie.
h = {}

for j in all_reviews:
    current_len = 0
    counter = 0
    browser.get(j)
    while True :
        browser.execute_script(f"window.scrollTo({current_len},{current_len+25000})")  # scroll function from length 0 to 25000 selenium
        try:
            search_button = browser.find_element_by_id('load-more-trigger') # selecting the load button in soup object
            time.sleep(0.5)  # give time to load page
            search_button.click() #click 
            current_len += 25000
            counter += 1
        except:
            break
        if counter > 2:
            break
    reviewss = browser.find_elements_by_class_name('review-container') # getting all reviews from soup
    #browser.execute_script("window.scrollTo(0, 50000)")
    u = []
    for i in reviewss:
        l = i
        try:
            dropdown_button = l.find_element_by_class_name('expander-icon-wrapper spoiler-warning__control')# selecing dropdown 
            if drowdown_button:
                l = dropdown_button.click() # click it 
        except:
            pass
        txt = l.find_element_by_class_name("content").text # selecting all content
        txt = re.sub(r'[0-9]+\sout\sof.*','',txt,re.DOTALL) # to clean text
        txt = re.sub(r'[Pp]ermalink.*','',txt,re.DOTALL ) # to clean permalink in text 
        txt = txt.replace(' ,',',') # to clean space before the commas
        txt = ' '.join(txt.split()) # clean white space > 1 to single white space
        u.append(txt)
    
    u = [' '.join(i.split('\n')) for i in u if len(i) > 1] # remove new line and replace it with single white space
    h[j] = u

df['reviews_text'] = df['reviews_url'].map(h) # mapping urls with reviews_text

# looping through all the reviews to score, get average of scores, stdev, number of reviews in each movie
url_keys = {}
for f in h.keys():
    scores = []
    list_reviews = h[f]
    for p in list_reviews:
        reviewed = Sentence(p) 
        classifier.predict(reviewed) # prediting the reviews
        thescore = reviewed.labels[0].score # scoring all the reviews with flair
        scores.append(thescore)
    url_keys[f] = {'scores': scores,'average': statistics.mean(scores), 'stdev': statistics.stdev(scores), 'number_reviews': len(scores)}
    
averages = {}
std = {}
number_of_reviews = {}
for i in url_keys.keys():
    averages[i] = url_keys[i]['average'] # getting all average of scores from dictionary
    number_of_reviews[i] = url_keys[i]['number_reviews'] # getting all reviews from dictionary
    std[i] = url_keys[i]['stdev'] # getting all stdev from dictionary

df['average_sentiment'] = df['reviews_url'].map(averages) #mapping average sentiment to reviews url
df['number_of_reviews'] = df['reviews_url'].map(number_of_reviews) # mapping number of reviews to reviews url
df['stdev_sentiment'] = df['reviews_url'].map(std) # mapping all stdev to reviewws url

df['rating']= df.rating.astype(float) # converting the rating cloumn to float values
df['year'] = df['year'].astype(int) # converting yearto interger values

df['weighted_sentiment'] = df.average_sentiment * 10 # weighing the average sentiment to rating of imdb 

df.to_csv('imdb_final.csv') # saving the dataframe as csv 