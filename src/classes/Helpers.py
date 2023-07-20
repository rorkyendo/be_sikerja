from datetime import datetime
import jaro

class Helpers():
    @staticmethod
    def days_between(d1):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.now()
        return (d1 - d2).days

    @staticmethod
    def similarity_score(word1, word2):
        return jaro.jaro_winkler_metric(word1, word2)