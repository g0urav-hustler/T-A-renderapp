
from flask import Flask , render_template, request
import json
import urllib
import os

IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


@app.route('/', methods = ['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/sentiment_analysis', methods = ['GET','POST'])
def sent_analysis():
    text = request.form['text']

    url = "https://1wna3xut2i.execute-api.us-east-1.amazonaws.com/Thought-anlyzer-app/predict_func"
   
    # url = "https://1wna3xut2i.execute-api.us-east-1.amazonaws.com/Thought-anlyzer-app/predict_func"
   
# text = "you are so special for me what can i say to you ."
# urllib.request.urlopen(url= url, data = data)

    data = {
    "thought": str(text)
    }
    data = json.dumps(data)
    print(data)
    data = str(data)
    data = data.encode("utf-8")


    resp = urllib.request.urlopen(url= url, data = data)

    prediction = resp.read()
    prediction = json.loads(prediction)


    pos = prediction["Positive Percentage "]
    neg = prediction["Negative Percentage "]
    sent = prediction["Sentiment"]

    sentiment = f"In your thought, there is {pos} positivity and {neg} negetivity. Overall it was {sent} thought. "



    if pos > neg:
        percentage = pos
        img_file = os.path.join(IMAGE_FOLDER, 'Smiling_Emoji.png')

    else:
        percentage = neg
        img_file = os.path.join(IMAGE_FOLDER, 'Sad_Emoji.png')

    

    return render_template('home.html', text = text, sentiment = sentiment, sent_percent = percentage, image = img_file)


if __name__ == "__main__":
    app.run(debug = True)
