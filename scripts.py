from API_requests import *


def str_rank_to_int(league, division, league_points):
    league_multipliers = {
        "IRON": 0,
        "BRONZE": 1,
        "SILVER": 2,
        "GOLD": 3,
        "PLATINUM": 4,
        "DIAMOND": 5,
        "MASTER": 6,
        "GRANDMASTER": 6,
        "CHALLENGER": 6
    }

    division_multipliers = {
        "IV": 0,
        "III": 1,
        "II": 2,
        "I": 3
    }

    rank_int = 0.0001 * league_points +\
                (1 * division_multipliers[division]) +\
                (10 * league_multipliers[league])

    return rank_int












