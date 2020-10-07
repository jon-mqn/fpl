import asyncio
from operator import attrgetter

import aiohttp
from prettytable import PrettyTable

from fpl import FPL
from fpl.utils import team_converter

def get_gameweek_score(player, gameweek):
    gameweek_history = next((history for history in player.history if history["round"] == gameweek), None)
    if gameweek_history is None:
        return 0
    else:
        return gameweek_history["total_points"]

def get_scores(player):
    scores = {}
    for history in player.history:
        scores[history["round"]]=history["total_points"]
    return scores

async def main(user_id):
    player_table = PrettyTable()
    player_table.field_names = ["Gameweek", "Player", "Points"]
    player_table.align = "r"

    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        user = await fpl.get_user(user_id)
        picks = await user.get_picks()

        for gameweek, elements in picks.items():
            players = await fpl.get_players([player["element"] for player in elements], include_summary=True)
            
            print(f'~~Team for gameweek {gameweek}~~')
            for player in players:
                player_scores = get_scores(player)
                for round, score in player_scores.items():
                    print(','.join([player.web_name, str(round), str(score)]))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(1986437))
    # https://github.com/aio-libs/aiohttp/issues/4324
    # asyncio.run(main(1986437))
