"""Probability & Games calculators."""
import math
import random
from .base import Calculator, CalcResult, InputField, fmt


class DiceProbabilityCalc(Calculator):
    id = "game_dice"
    name = "Dice Probability"
    category = "Probability & Games"
    description = "Probability of rolling a sum with two dice"
    icon = "🎲"
    example = "Sum 7 with two dice → 6/36 = 16.7%"

    def get_inputs(self):
        return [
            InputField("dice", "Number of dice", "number", 2),
            InputField("target", "Target sum", "number", 7),
        ]

    def calculate(self, values):
        dice = int(self.num(values, "dice"))
        target = int(self.num(values, "target"))
        if dice < 1 or dice > 8:
            raise ValueError("Use 1 to 8 dice")
        # Count ways via dynamic programming
        ways = {0: 1}
        for _ in range(dice):
            new = {}
            for s, c in ways.items():
                for face in range(1, 7):
                    new[s + face] = new.get(s + face, 0) + c
            ways = new
        total = 6 ** dice
        ways_target = ways.get(target, 0)
        p = ways_target / total
        return [
            CalcResult("Ways to roll target", f"{ways_target:,}"),
            CalcResult("Total outcomes", f"{total:,}"),
            CalcResult("Probability", f"{fmt(p * 100, 4)}%"),
            CalcResult("Odds", f"{fmt(ways_target,0)} : {fmt(total - ways_target,0)}"),
        ]


class CardProbabilityCalc(Calculator):
    id = "game_cards"
    name = "Card Probability"
    category = "Probability & Games"
    description = "Probability of drawing cards from a standard deck"
    icon = "🃏"
    example = "Drawing an Ace → 4/52 = 7.7%"

    def get_inputs(self):
        return [
            InputField("favorable", "Favorable cards", "number", 4),
            InputField("drawn", "Cards drawn (without replacement)", "number", 1),
        ]

    def calculate(self, values):
        fav = int(self.num(values, "favorable"))
        drawn = int(self.num(values, "drawn"))
        if drawn < 1 or drawn > 10:
            raise ValueError("Draw between 1 and 10 cards")
        if fav < 0 or fav > 52:
            raise ValueError("Favorable cards between 0 and 52")
        # Probability of at least one favorable card in `drawn` draws without replacement
        total = 52
        if fav >= total - (drawn - 1):
            p = 1.0
        else:
            p = 1
            for i in range(drawn):
                p *= (total - fav - i) / (total - i)
            p = 1 - p
        return [
            CalcResult("Chance of at least one", f"{fmt(p * 100, 3)}%"),
            CalcResult("As odds", f"1 in {fmt(1 / p if p else float('inf'), 1)}"),
            CalcResult("Deck remaining", total - drawn),
        ]


class LotteryOddsCalc(Calculator):
    id = "game_lottery"
    name = "Lottery Odds"
    category = "Probability & Games"
    description = "Odds of winning a pick-k lottery"
    icon = "🎟️"
    example = "6 of 49 → 1 in 13,983,816"

    def get_inputs(self):
        return [
            InputField("pick", "Numbers to pick", "number", 6),
            InputField("range", "Number range", "number", 49),
        ]

    def calculate(self, values):
        k = int(self.num(values, "pick"))
        n = int(self.num(values, "range"))
        if k < 1 or n < k or k > 60:
            raise ValueError("Pick must be between 1 and range (max 60)")
        combos = math.comb(n, k)
        return [
            CalcResult("Total combinations", f"{combos:,}"),
            CalcResult("Odds", f"1 in {combos:,}"),
            CalcResult("Probability", f"{fmt(1 / combos * 100, 12)}%"),
        ]


class WinningPercentageCalc(Calculator):
    id = "game_winning_pct"
    name = "Winning Percentage"
    category = "Probability & Games"
    description = "Win percentage for a team/player"
    icon = "🏆"
    example = "Won 12, lost 3 → 80%"

    def get_inputs(self):
        return [
            InputField("wins", "Wins", "number", 12),
            InputField("losses", "Losses", "number", 3),
            InputField("ties", "Ties (optional)", "number", 0, required=False),
        ]

    def calculate(self, values):
        wins, losses = self.num(values, "wins"), self.num(values, "losses")
        ties = self.num(values, "ties")
        total = wins + losses + ties
        if total == 0:
            raise ValueError("Total games cannot be zero")
        pct = wins / total * 100
        return [
            CalcResult("Winning percentage", f"{fmt(pct, 2)}%"),
            CalcResult("Total games", fmt(total)),
            CalcResult("Win-loss record", f"{fmt(wins,0)}-{fmt(losses,0)}-{fmt(ties,0)}"),
        ]


class SportsStatisticsCalc(Calculator):
    id = "game_sports"
    name = "Sports Statistics"
    category = "Probability & Games"
    description = "Batting average / shooting percentage"
    icon = "⚽"
    example = "120 runs in 40 balls → strike rate 300"

    def get_inputs(self):
        return [
            InputField("success", "Successful attempts", "number", 120),
            InputField("total", "Total attempts", "number", 40),
            InputField("type", "Stat type", "select", "Strike rate", options=[
                "Batting average", "Strike rate", "Shooting percentage", "Pass completion",
            ]),
        ]

    def calculate(self, values):
        success, total = self.num(values, "success"), self.num(values, "total")
        if total == 0:
            raise ValueError("Total attempts cannot be zero")
        stat_type = values.get("type", "Strike rate")
        if stat_type == "Batting average":
            val = success / total
            label = "Average"
            extra = f"{fmt(success,0)} runs in {fmt(total,0)} innings"
        elif stat_type == "Strike rate":
            val = success / total * 100
            label = "Strike rate"
            extra = f"{fmt(success,0)} runs in {fmt(total,0)} balls"
        else:
            val = success / total * 100
            label = "Percentage"
            extra = f"{fmt(success / total * 100, 1)}%"
        return [
            CalcResult(label, fmt(val, 2)),
            CalcResult("Raw ratio", f"{fmt(success,0)}/{fmt(total,0)}"),
            CalcResult("Detail", extra),
        ]
