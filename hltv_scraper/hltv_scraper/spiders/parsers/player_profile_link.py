from .parser import Parser

class PlayerProfileLinkParser(Parser):
    @staticmethod
    def parse(response, player: str):
        return response.css(f"a[href^='/player/'][href$='/{player}']").getall()
        