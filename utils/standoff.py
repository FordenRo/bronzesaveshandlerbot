import re
from dataclasses import dataclass


@dataclass
class GivenItem:
    id: int
    nickname: str
    amount: float
    date: str

    @classmethod
    def parse_item(cls, text: str):
        kwargs = re.match(
            'ID:(?P<id>\\d+)\\(?(?P<nickname>\\w*)\\)?\nAmount:(?P<amount>[0-9.]+)G\nDate:(?P<date>[0-9.]+)',
            text.replace(' ', '')).groupdict()
        kwargs['id'] = int(kwargs['id'])
        kwargs['amount'] = float(kwargs['amount'])
        return cls(**kwargs)

    def to_text(self):
        return '\n'.join([f'ID: {self.id}{f' ({self.nickname})' if self.nickname else ''}',
                          f'{'Amount:':<9s}{self.amount:.2f} G',
                          f'{'Date:':<9s}{self.date}'])

    @classmethod
    def parse_all(cls, text: str):
        return [cls.parse_item(item) for item in text.split('\n\n')]

    @staticmethod
    def items_to_text(items: ['GivenItem']):
        return '\n\n'.join([i.to_text() for i in items])


@dataclass
class BoughtItem:
    name: str
    price: float
    amount: int
    date: str

    @classmethod
    def parse_item(cls, text):
        kwargs = re.match(
            '— (?P<name>.+) —\nAmount:\\s+(?P<amount>\\d+)\nPrice:\\s+(?P<price>[0-9.]+) G\nDate:\\s+(?P<date>[0-9.]+)',
            text).groupdict()
        kwargs['amount'] = int(kwargs['amount'])
        kwargs['price'] = float(kwargs['price'])
        return cls(**kwargs)

    def to_text(self):
        return '\n'.join([f'— {self.name} —',
                          f'{'Amount:':<9s}{self.amount:d}',
                          f'{'Price:':<9s}{self.price:.2f} G',
                          f'{'Date:':<9s}{self.date}'])

    @classmethod
    def parse_all(cls, text: str):
        return [cls.parse_item(item) for item in text.split('\n\n')]

    @staticmethod
    def items_to_text(items: ['BoughtItem']):
        return '\n\n'.join([i.to_text() for i in items])
