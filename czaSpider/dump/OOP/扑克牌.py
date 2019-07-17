import collections
import random

Card = collections.namedtuple('Card', ['rank', 'suit'])
suit_value = dict(clubs=0, diamonds=1, hearts=2, spades=3)  # 黑桃最大、红桃次之、方块再次、梅花最小


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)  # 下标
    return rank_value * len(suit_value) + suit_value[card.suit]  # 这就是算法的魅力吗


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'clubs diamonds hearts spades'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks
                       for suit in self.suits]

    def random_card(self):
        return random.choice(self._cards)

    @classmethod
    def new_cards(cls):
        return cls()

    def shuffle_cards(self):
        random.shuffle(self._cards)
        return self

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


if __name__ == '__main__':
    cards = FrenchDeck()
    cards.shuffle_cards()
    for card in cards._cards:
        print(card)
    # print(len(cards))
    # print(cards[:3])
    # print(cards.random_card().rank)
    # for card in sorted(cards, key=spades_high):
    #     print(card)

"""
__len__这类特殊方法的存在是为了被解释器调用的，我们应该尽量还用len()方法
对于python内置类型如list和str，CPython会抄近路，__len__实际上返回的是PyVarObject里面的on_size属性，此属性表示内存中长度可变的内置对象的C语言结构体，直接读值比调方法快很多
len()不是普通方法，CPython会直接从一个C结构体中读取对象的长度，完全不会盗用任何方法

很多时候特殊方法的调用是隐式的，比如for i in x:语句，背后调用的其实是iter(x)，而此函数背后又是x.__iter__()方法

"""
