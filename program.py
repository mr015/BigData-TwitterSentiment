import re 
import tweepy
import csv
import nltk
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from tweepy import OAuthHandler 
from textblob import TextBlob
from nltk.corpus import wordnet

from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.collocations import *
         
consumer_key = 'yIVix694ss0avN9Qffc2zprva'
consumer_secret = 'AQeHMLH2mFwhjozjvpRGgfbHU9h2Y6meiK9SHg1uICKNgvIK0R'
access_token = '2914060624-3l0tk0vUZnsiWcOGvGF3vGR6jYJNUJuj3S3xOi6'
access_token_secret = 'uJEmK3UPEN82YP6o0FsOX0Di610w7xNTfqfsJnvDZvDrH'
auth = OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth,wait_on_rate_limit=True) 
def clean_tweet(tweet):
                
        clean_text = re.sub(r"http\S+", "", tweet)
 
        clean_text = re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Zaz_]+[A-Za-z0-9-_]+)","", clean_text)
 
        clean_text = re.sub(u"[\U0001F000-\U0001F999]+", "",clean_text, flags=re.UNICODE)
        print("Tweets cleaning is done")
        #print(clean_text)
        return clean_text;
csvFile = open('tweets.csv', 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)
st_w= get_stop_words('en')
stemmer=SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()
lemtok=open('lemmatokens.csv', 'a', encoding="utf-8")
tokenWriter= csv.writer(lemtok)
se = open('sentiments.csv', 'a', encoding="utf-8")
senWriter = csv.writer(se)
occufile=open('occurrences.csv', 'a', encoding="utf-8")
occuWriter=csv.writer(occufile)
csvWriter.writerow(['Tweet ID','Username','Text','Number of Retweets','Number of Likes'])
tokenWriter.writerow(['Cleaned Text', 'Stemmed Tokens','Tweet ID'])
senWriter.writerow(['Text', 'sentiment polarity', 'sentiment subjectivity', 'tweet ID'])
occuWriter.writerow(['word','number of occurrences'])
n=0
nocc_c = {}
words = {}
for tweet in tweepy.Cursor(api.search,q="#politics",lang="en").items(1000):
        csvWriter.writerow([tweet.id, tweet.user.screen_name, tweet.text.encode("utf-8"), tweet.retweet_count, tweet.favorite_count])
        
        parsed_tweet = {} 
        cleantxt = clean_tweet(tweet.text)
        tk=nltk.word_tokenize(cleantxt)
        stp=[i for i in tk if not i in st_w]
        lemm=[lemmatizer.lemmatize(i) for i in stp]
        stemmed=[stemmer.stem(i) for i in lemm]
        tokenWriter.writerow([cleantxt,stemmed,tweet.id])
        
        anal = TextBlob(tweet.text)
        sent_pol=anal.sentiment.polarity
        sent_subj=anal.sentiment.subjectivity
        senWriter.writerow([cleantxt,sent_pol,sent_subj,tweet.id])
        
        nocc = ngrams(stemmed,1)
        for t in nocc:
                if t not in nocc_c:
                        nocc_c[t] = 1
                else:
                        nocc_c[t] += 1
                words[t]=t
                                                
for d in nocc_c:
        occuWriter.writerow([words[d],nocc_c[d]])
        
                        
csvFile.close()
lemtok.close()
se.close()
occufile.close()

                

