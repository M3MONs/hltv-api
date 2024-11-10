from .parser import Parser


class PlayerProfileStatsParser(Parser):
    @staticmethod
    def parse(stats):
        return [
            {
                f'{stat.css("b::text").get()}': stat.css("span.statsVal p::text").get(),
            }
            for stat in stats
        ]
