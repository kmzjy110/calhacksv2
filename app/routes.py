
from flask import Flask, render_template, request

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def transcribe_emotion(score):
    emotion = ""
    if 0.1 >= score >= -0.1:
        emotion = "Mixed/Neutral"
    elif 0.1 <= score <= 0.5:
        emotion = "Moderately Positive"
    elif score >= 0.5:
        emotion = "Clearly Positive"
    elif -0.5 <= score <= -0.1:
        emotion = "Moderately Negative"
    else:
        emotion = "Clearly Negative"
    return emotion


def analyze(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    analyzations = client.analyze_sentiment(document=document)
    overall = analyzations.document_sentiment
    out = []
    for sentence in analyzations.sentences:
        out.append( "Content:" + sentence.text.content + "\n")
        out.append("Sentiment:" + transcribe_emotion(sentence.sentiment.score) + "\n")
    out.append("Overall Sentiment:" + transcribe_emotion(overall.score))
    return out

app=Flask(__name__)
@app.route('/',methods=['GET', 'POST'])
def index():
    with app.app_context():

        if request.form:

            body = request.form.get('body')
            out=analyze(body)
            return render_template("home.html", out=out)
    return render_template("home.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)