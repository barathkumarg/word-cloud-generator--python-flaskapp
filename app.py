# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 18:15:39 2020

@author: barathkumar
"""

from flask import Flask, request, jsonify, render_template,send_file,redirect
import sys
import numpy as np
from PIL import Image
import wikipedia
from wordcloud import WordCloud,STOPWORDS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/home1')
def home1():
    return render_template('home.html')

@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/predict',methods=['POST'])
def predict():
    x=request.form['title']
    b=request.form['color']
    
    c=int(request.form['words'])
    option = request.form['options']
    title=wikipedia.search(x)[0]
    page=wikipedia.page(title)
    text=page.content

    background=np.array(Image.open("cloud.png"))
    stopwords=set(STOPWORDS)
    wc=WordCloud(background_color=b,
				max_words=c,
				mask=background,
				stopwords=stopwords)

    wc.generate(text)
    wc.to_file("{0}.{1}".format(x,option))
    return send_file(("{0}.{1}".format(x,option)),as_attachment=True)
    
@app.route('/predict1',methods=['POST'])
def predict1():
    f = request.form['filename'] 
    
    b=request.form['color']
    c=int(request.form['words'])
    stopwords=set(STOPWORDS)
    
    option = request.form['options']
    with open(f, "r") as f:
        words = f.read().split()

    data = dict()

    for word in words:
        word = word.lower()
        if word in stopwords:
            continue

        data[word] = data.get(word, 0) + 1
    background=np.array(Image.open("cloud.png"))
    word_cloud = WordCloud(
            background_color=b,
            max_words=c,
			mask=background,
			stopwords=stopwords
            )

    word_cloud.generate_from_frequencies(data)
    word_cloud.to_file("{0}.{1}".format("Result",option))
    return send_file(("{0}.{1}".format("Result",option)),as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)