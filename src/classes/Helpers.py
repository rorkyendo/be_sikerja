import jellyfish
from datetime import datetime

class Helpers():
    @staticmethod
    def days_between(d1):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.now()
        return (d1 - d2).days

    @staticmethod
    def similarity_score(word1, word2):
        return jellyfish.jaro_winkler(word1, word2)
