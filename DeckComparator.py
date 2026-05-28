class Comparison_Results:
    def __init__(self, deck1_unique_cards: dict, deck2_unique_cards: dict, differing_card_numbers: dict, shared_cards: dict):
        self.deck1_unique_cards = deck1_unique_cards
        self.deck2_unique_cards = deck2_unique_cards
        self.differing_card_numbers = differing_card_numbers
        self.shared_cards = shared_cards

def compare_mainboards(mainboard1: dict, mainboard2: dict) -> Comparison_Results:
    deck1_unique_cards = {}
    deck2_unique_cards = {}
    differing_card_numbers: dict[str, dict[str, int]] = {"Deck1" : {}, "Deck2" : {}}
    shared_cards = {}
    
    for card_name, details in mainboard1.items():
        count = details.get('quantity', 1)
        if card_name not in mainboard2:
            deck1_unique_cards[card_name] = count
        elif count != mainboard2[card_name].get('quantity', 1):
            differing_card_numbers["Deck1"][card_name] = count
            differing_card_numbers["Deck2"][card_name] = mainboard2[card_name].get('quantity', 1)
        else:
            shared_cards[card_name] = count
    
    for card_name, details in mainboard2.items():
        count = details.get('quantity', 1)
        if card_name not in mainboard1:
            deck2_unique_cards[card_name] = count
    
    return Comparison_Results(deck1_unique_cards, deck2_unique_cards, differing_card_numbers, shared_cards)