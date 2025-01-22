"""Minimal The Eyes Have It game """
from card_library.card_deck import CardDeck
from card_library.face_card import FaceCard
from card_library.game_hand import GameHand


def score(hand):
    """compute a score of hand"""
    eye_count = 0
    rank_count = 0
    for card in hand.cards:
        if isinstance(card, FaceCard):
            eye_count += card.eyes
        else:
            rank_count += card.rank
    return rank_count * eye_count


deck = CardDeck()
system_hand = GameHand()
player_hand = GameHand()

for i in range(0, 5):
    deck.shuffle()
    system_hand.insert(deck.deal())
    player_hand.insert(deck.deal())

print("Player:", player_hand, score(player_hand))
print("System:", system_hand, score(system_hand))
diff = score(player_hand) - score(system_hand)

if diff > 0:
    print("You won by", diff, "points")
elif diff < 0:
    print("You lost by", -diff, "points")
else:
    print("Tied hand")
player_hand.return_cards_to_deck(deck)
system_hand.return_cards_to_deck(deck)
