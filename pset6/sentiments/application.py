from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer

import sys
from nltk.tokenize import TweetTokenizer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    try :
        tweets = helpers.get_user_timeline(screen_name, 100)
    except RuntimeError as err :
        print(err)

    # instantiate tockenizer
    tokenizer = TweetTokenizer()

    # initialize tweet count
    positive, negative, neutral = 0.0, 0.0, 0.0

    # set absolute dictionary path
    positives = "positive-words.txt"
    negatives = "negative-words.txt"

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)

    try:
        for tweet in tweets :

            #reset score for each tweet
            score = 0
            for word in tokenizer.tokenize(tweet) :
                score = score + analyzer.analyze(word)

            # increment tweet type
            if score < 0 :
                negative += 1
            elif score > 0  :
                positive += 1
            else :
                neutral += 1

    except TypeError :
        sys.stderr.write("WRONG screen_name\n")


    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
