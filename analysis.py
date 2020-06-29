try:
    # Sentiment Analysis
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # Graph imports
    import matplotlib.pyplot as plt
except ImportError:
    import sys
    import subprocess
    print("[NOT IMPORTED]")
    subprocess.call([sys.executable, "-m", "pip", "install", "matplotlib"])
    print("[INSTALLED MATPLOTLIB]")
    subprocess.call([sys.executable, "-m", "pip", "install", "vaderSentiment"])
    print("[INSTALLED VADER SENTIMENT]")
    print("[CONTINUE]")

# Find sentiment of chat
try:
    from server_and_GUI import messages
except ImportError as err:
    print(f"[ERROR]: {err}")


class SentimentAnalysis:
    def __init__(self):
        self.all_score = self
        self.score = self
        self.li_of_scores = []
        self.compound_list = []
        self.sentence = self
        self.negative_score = self
        self.positive_score = self
        self.neutral_score = self
        self.overall = self

    def sentiment_score(self, list_of_messages):
        analyze = SentimentIntensityAnalyzer()
        neg = 0
        pos = 0
        neu = 0
        # Giving score for each area
        for message in list_of_messages:
            sentiment_dict = analyze.polarity_scores(message)
            self.negative_score = sentiment_dict['neg'] * 100
            self.positive_score = sentiment_dict['pos'] * 100
            self.neutral_score = sentiment_dict['neu'] * 100

            self.li_of_scores.append((self.negative_score, self.positive_score))

            # decide sentiment as positive, negative and/or neutral
            if sentiment_dict['compound'] >= 0.05:
                self.score = 'positive'
                self.compound_list.append(self.score)

            elif sentiment_dict['compound'] <= - 0.05:
                self.score = 'negative'
                self.compound_list.append(self.score)

            else:
                self.score = 'neutral'
                self.compound_list.append(self.score)

        for score in self.compound_list:
            if score == ['positive']:
                pos += 1
            elif score == ['negative']:
                neg += 1
            else:
                neu += 1

        if pos > neg:
            self.overall = 'positive'
        elif neg > pos:
            self.overall = 'negative'
        else:
            self.overall = 'neutral'

        sen = SentimentAnalysis()
        sen.graph()
        return self.overall, self.li_of_scores

    def graph(self):
        plt.title("Sentiment of Messages")
        plt.plot(self.li_of_scores, color='m', marker='o', markerfacecolor='g', linestyle='dotted', linewidth=2)
        plt.xlabel("Message #")
        plt.ylabel("Sentiment of Message")
        plt.show()
