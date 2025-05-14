from enum import Enum

class TradeType(Enum):
    BUY = 'buy'
    SELL = 'sell'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.capitalize()) for tag in cls] 