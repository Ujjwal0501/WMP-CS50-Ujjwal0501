import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        file = open(positives, "r")
        self.positives = set()
        for line in file :
            if line.startswith(";") == False:
                self.positives.add(line.strip("\n"))

        file = open(negatives, "r")
        self.negatives = set()
        for line in file :
            if line.startswith(";") == False :
                self.negatives.add(line.strip("\n"))

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        sum = 0
        if text.lower() in self.positives :
            sum = sum + 1
        elif text.lower() in self.negatives :
            sum = sum - 1
        else :
            sum = sum

        return sum
