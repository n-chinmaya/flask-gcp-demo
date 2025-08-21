from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

def get_sentiment(polarity):
    """ Classify the polarity score into a descriptive sentiment with an emoji. """
    if polarity > 0.6:
        return "Very Positive 😀"
    elif polarity > 0.2:
        return "Positive 🙂"
    elif polarity >= -0.2:
        return "Neutral 😐"
    elif polarity > -0.6:
        return "Negative 😠"
    else:
        return "Very Negative 😡"

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    if request.method == "POST":
        text = request.form.get("review", "")
        if text:
            blob = TextBlob(text)
            
            # Perform sentiment analysis
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Package the results into a dictionary
            analysis = {
                "text": text,
                "polarity": round(polarity, 2),
                "subjectivity": round(subjectivity, 2),
                "sentiment": get_sentiment(polarity),
                "noun_phrases": blob.noun_phrases
            }
            
    return render_template("index.html", analysis=analysis)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)