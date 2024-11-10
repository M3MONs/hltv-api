from .parser import Parser
from .match import MatchParser as MP

class ResultsParser(Parser):
    @staticmethod
    def parse(sublists):
        all_results = {}
        for sublist in sublists:
            date = sublist.css(".standard-headline::text").get()
            all_results[date] = [MP.parse(result) for result in sublist.css("a.a-reset")]
        return all_results