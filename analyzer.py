# analyzer.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def get_sentiment_label(text: str) -> str:
    score = _analyzer.polarity_scores(str(text))["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def get_sentiment_score(text: str) -> float:
    return _analyzer.polarity_scores(str(text))["compound"]