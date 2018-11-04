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
        out += "Content:" + sentence.text.content + "\n"
        out += "Sentiment:" + transcribe_emotion(sentence.sentiment.score) + "\n"
    out += "Overall Sentiment:" + transcribe_emotion(overall.score)
    print(out)
    return out

print(analyze("i hate u."))