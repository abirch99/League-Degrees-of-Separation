import requests
from time import sleep, time
from collections import deque


class API_calls:
    def __init__(self, server, region, API_key):
        self.API_key = API_key
        self.server = server
        self.region = region
    request_times_queue = deque(maxlen=100)


    def queue_handler(self):
        self.request_times_queue.append(time())
        if len(self.request_times_queue) == 100:
            time_diff = 120 - (time() - self.request_times_queue[0])

            if time_diff > 1:
                print("Sleeping: " + str(time_diff))
                sleep(time_diff)
            elif time_diff > 0:
                sleep(time_diff)
            else:
                pass

    
    def status_handler(self, status, body, func, *func_args):
        inherited_arg = func_args[0]

        if status == 429:
            print("429: Sleeping 120s")
            sleep(120)
            return func(inherited_arg)

        elif status == 403:
            print("403: Forbidden. Are you sure the API key is valid?")
            return None

        elif status == 200:
            return body

        elif status == 503:
            return func(inherited_arg)

        else:
            print("Error code: " + str(status))
            print("Sleeping 120s")
            sleep(120)
            return func(inherited_arg)


    def get_ids_by_summoner_name(self, summoner_name):
        '''
        Parameters:
                summoner_name -> Str: Takes string of summoner name as shown in game.
                server -> Str: Takes string of riot server.
                API_key -> Str: Takes string of riot API key.

        Return:
                {
                    "id": Str -> Encrypted summoner ID. Max length 63 characters,
                    "accountId": Str -> Encrypted account ID. Max length 56 characters,
                    "puuid": Str -> Encrypted PUUID. Exact length of 78 characters,
                    "name": Str -> Summoner Name,
                    "profileIconId": Int -> ID of the summoner icon associated with the summoner,
                    "revisionDate": LongInt -> Date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: summoner name change, summoner level change, or profile icon change,
                    "summonerLevel": LongInt -> Summoner level associated with the summoner
                }
        '''

        self.queue_handler()
        r = requests.get(f"https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={self.API_key}")
        status = r.status_code
        body = r.json()

        handled_body = self.status_handler(status, body, self.get_ids_by_summoner_name, summoner_name)
        return handled_body


    def get_ids_by_puuid(self, puuid):

        self.queue_handler()
        r = requests.get(f"https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.API_key}")
        status = r.status_code
        body = r.json()

        handled_body = self.status_handler(status, body, self.get_ids_by_puuid, puuid)
        try:
            reduced_body = {
                "id": handled_body["id"],
                "accountId": handled_body["accountId"],
                "puuid": handled_body["puuid"],
                "summoner_name": handled_body["name"],
            }
            return reduced_body

        except:
            return None


    def get_matches_by_puuid(self, puuid, queue_type=420):
        '''
        Parameters:
                puuid -> Str: Takes string of puuid.
                region -> Str: Takes string of region. != riot server.
                API_key -> Str: Takes string of API_key.
                queue_type -> Int: Takes int of queue type, default 420. {420: ranked, 400: normals}

        Return:
                List[Str] -> Max length 20. Contains strings of match IDs for that player. Match depends on specified queue type. Can be empty.
        '''

        self.queue_handler()
        r = requests.get(f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue_type}&start=0&count=20&api_key={self.API_key}")
        status = r.status_code
        body = r.json()

        handled_body = self.status_handler(status, body, self.get_matches_by_puuid, puuid)
        return handled_body


    def get_match_info_by_match_id(self, match_id):
        '''
        
        '''

        self.queue_handler()
        r = requests.get(f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.API_key}")
        status = r.status_code
        body = r.json()

        handled_body = self.status_handler(status, body, self.get_match_info_by_match_id, match_id)

        try:
            game_stats = {"winners": [], "losers": [], "stats": {}}

            game_stats["stats"]["game_type"] = handled_body["info"]["queueId"]
            game_stats["stats"]["duration"] = handled_body["info"]["gameDuration"]
            game_stats["stats"]["start_epoch"] = handled_body["info"]["gameCreation"]
            game_stats["stats"]["server"] = handled_body["info"]["platformId"]

            participants = handled_body["info"]["participants"]
            for player in participants:
                if player["win"] == True:
                    game_stats["winners"].append({
                        "puuid": player["puuid"],
                        "summoner_id": player["summonerId"],
                        "summoner_name": player["summonerName"],
                        "champion_name": player["championName"],
                        "lane": player["teamPosition"],
                        "role": player["role"],
                        "kills": player["kills"],
                        "deaths": player["deaths"],
                        "assists": player["assists"]
                        })

                else:
                    game_stats["losers"].append({
                        "puuid": player["puuid"],
                        "summoner_id": player["summonerId"],
                        "summoner_name": player["summonerName"],
                        "champion_name": player["championName"],
                        "lane": player["teamPosition"],
                        "role": player["role"],
                        "kills": player["kills"],
                        "deaths": player["deaths"],
                        "assists": player["assists"]
                        })
                
            return game_stats

        except:
            return None


    def get_summoner_stats_by_id(self, id):
        '''
        '''

        self.queue_handler()
        r = requests.get(f"https://{self.server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.API_key}")
        status = r.status_code
        body = r.json()[0]

        handled_body = self.status_handler(status, body, self.get_summoner_stats_by_id, id)

        try:
            reduced_body = {
                "summoner_name": handled_body["summonerName"],
                "summoner_id": handled_body["summonerId"],
                "league": handled_body["tier"],
                "division": handled_body["rank"],
                "league_points": handled_body["leaguePoints"],
                "wins": handled_body["wins"],
                "losses": handled_body["losses"]
            }
            return reduced_body

        except:
            return None


    def get_loser_ids_from_match_ids(self, match_id_list, player_ids):

        loss_match_ids = []
        match_limit = 1

        for match_id in match_id_list:
            if len(loss_match_ids) < match_limit:
                match_stats = self.get_match_info_by_match_id(match_id)
                winners_list = match_stats["winners"]

                for player in winners_list:
                    if player["puuid"] == player_ids["puuid"]:
                        loss_match_ids.append({
                                                match_id: match_stats["losers"]
                                                })
                        break

        return loss_match_ids







