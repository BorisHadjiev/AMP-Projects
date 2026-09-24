"""ALGOGEM Bot - This is the file you edit to create your bot!

Implement your strategy by editing the MyBot class below.
Run with: python algogem_client.py --server <ip> --token <token> --mode practice

Data types available to you:
    GemType      - Enum: GREEN, BLUE, PINK, PURPLE, ORANGE
    AuctionCard  - Has auction_type ("treasure_1", "treasure_2", "loan", "invest")
                   and value (loan/invest amount, None for treasure)
    MissionCard  - Has mission_id, required_gems, reward, mission_type, wildcard_count

State tracked for you by the base class (access via self.*):
    coins          - Your current coin balance
    hand           - Your current hand (list of GemType)
    collection     - Gems you've won in auctions (list of GemType)
    player_coins   - All players' coin balances {player_id: coins}
    revealed_cards - Cards in the value display {GemType: count}
    available_gems - Gems currently available for auction (list of GemType)
    player_names   - Names of all players [str, ...]
"""

from algogem_client import AlgogemBot, AuctionCard, GemType, MissionCard  # noqa: F401

from copy import deepcopy

import math

import random

class MyBot(AlgogemBot):
    """Your bot - implement the two required methods below.

    The base class automatically tracks game state for you:
        self.coins           - Your current coin balance
        self.hand            - Your current hand (list of GemType)
        self.collection      - Gems you've won in auctions
        self.player_coins    - All players' coin balances {player_id: coins}
        self.revealed_cards  - Cards in the value display {GemType: count}
        self.available_gems  - Gems currently available for auction
        self.player_names    - Names of all players [str, ...]
    """

    # --- REQUIRED: You must implement these two methods ---


    def build_hidden_gems(self):

        total_information = {gem: self.revealed_cards.get(gem, 0) for gem in GemType}
 
        if self.hand:
            for gem in self.hand:
                total_information[gem] = total_information.get(gem, 0) + 1
 
        for gem in self.available_gems:
            total_information[gem] = total_information.get(gem, 0) + 1
 
        for gem in self.collection:
            total_information[gem] = total_information.get(gem, 0) + 1
 
        return {gem: max(0, 6 - total_information.get(gem, 0)) for gem in GemType}
 
    def simulate_reveal_outcomes(self, hidden_gems, gem_colors, num_simulations=3000):
    
        revealed_card_number = sum(self.revealed_cards.values())
        if self.hand:
            revealed_card_number += len(self.hand)
        total_unrevealed_cards = max(1, 22 - revealed_card_number)
 
        hidden_bag = []
        for gem, count in hidden_gems.items():
            hidden_bag.extend([gem] * count)
 
        if not hidden_bag:
            return 0.0, 0.0
 
        future_slots = min(total_unrevealed_cards, len(hidden_bag))
 
        totals = []
        for _ in range(num_simulations):
            sample = random.sample(hidden_bag, future_slots)
            totals.append(sum(1 for gem in sample if gem in gem_colors))
 
        mean = sum(totals) / num_simulations
        variance = sum((x - mean) ** 2 for x in totals) / num_simulations
        return mean, variance ** 0.5
 
    def estimate_value(self, gem_colors, hidden_gems, num_simulations=3000):

        mean_future, std_future = self.simulate_reveal_outcomes(
            hidden_gems, gem_colors, num_simulations
        )
        revealed_total = sum(self.revealed_cards.get(g, 0) for g in gem_colors)
 
        mean_value = (revealed_total + mean_future / 2) * 4
        std_value = std_future * 2  
        return mean_value, std_value
 
 
    def get_bid_value(self, bid):
        return bid if bid <= self.coins else self.coins
 
    def get_bid(
        self, auction_card: AuctionCard, available_gems: list[GemType]
    ) -> int:
        """Return your bid amount for this auction."""
        try:
            total_revealed_cards = sum(self.revealed_cards.values())
            revealed_cards_percentage = min(total_revealed_cards / 26, 1.0)
            bet_multiplier = round(0.65 + 0.2 * revealed_cards_percentage, 2)

            risk_aversion = 0.5
 
            if auction_card.auction_type == "treasure_1":
                hidden_gems = self.build_hidden_gems()
                mean_value, std_value = self.estimate_value(
                    {available_gems[0]}, hidden_gems
                )
                risk_adjusted = max(0.0, mean_value - risk_aversion * std_value)
                bid = int(risk_adjusted * bet_multiplier) + 1
                return self.get_bid_value(bid)
 
            if auction_card.auction_type == "treasure_2":
                hidden_gems = self.build_hidden_gems()
                mean_value, std_value = self.estimate_value(
                    {available_gems[0], available_gems[1]}, hidden_gems
                )
                risk_adjusted = max(0.0, mean_value - risk_aversion * std_value)
                bid = int(risk_adjusted * bet_multiplier) + 1
                return self.get_bid_value(bid)
 
            if auction_card.auction_type == "loan":
                revealed_card_number = sum(self.revealed_cards.values())
                if revealed_card_number <= 5:
                    if auction_card.value == 10:
                        return self.get_bid_value(3)
                    if auction_card.value == 20:
                        return self.get_bid_value(7)
                else:
                    return 0
 
            if auction_card.auction_type == "invest":
                revealed_card_number = sum(self.revealed_cards.values())
                if auction_card.value == 5:
                    if revealed_card_number <= 7:
                        return self.get_bid_value(6)
                    else:
                        return self.get_bid_value(7)
                if auction_card.value == 10:
                    if revealed_card_number <= 7:
                        return self.get_bid_value(9)
                    elif revealed_card_number <= 10:
                        return self.get_bid_value(10)
                    else:
                        return self.get_bid_value(11)
        except Exception:
            return 5
 
    def evaluate_reveal_choice(self, candidate_index, hidden_gems, num_simulations=1500):
        hand_after = list(self.hand)
        revealed_gem = hand_after.pop(candidate_index)
 
        hypothetical_revealed = dict(self.revealed_cards)
        hypothetical_revealed[revealed_gem] = hypothetical_revealed.get(revealed_gem, 0) + 1
 
        hypothetical_hidden = dict(hidden_gems)
        if hypothetical_hidden.get(revealed_gem, 0) > 0:
            hypothetical_hidden[revealed_gem] -= 1
 
        original_revealed, original_hand = self.revealed_cards, self.hand
        self.revealed_cards, self.hand = hypothetical_revealed, hand_after
        try:
            my_gem_colors = set(self.collection) | set(hand_after)
            mean_value, _ = self.estimate_value(
                my_gem_colors, hypothetical_hidden, num_simulations
            ) if my_gem_colors else (0.0, 0.0)
        finally:
            self.revealed_cards, self.hand = original_revealed, original_hand
 
        return mean_value
 
    def choose_card_to_reveal(self, hand: list[GemType]) -> int:

        if not hand:
            return 0
        if len(hand) == 1:
            return 0
 
        hidden_gems = self.build_hidden_gems()
 
        best_index = 0
        best_value = None
        for index in range(len(hand)):
            value = self.evaluate_reveal_choice(index, hidden_gems)
            if best_value is None or value > best_value:
                best_value = value
                best_index = index
 
        return best_index