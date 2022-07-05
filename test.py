import requests
from time import sleep, time
from collections import deque

file = open("API_keys.txt", "r")
API_key = file.readlines()[0]
file.close()


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
            if time_diff > 0:
                sleep(time_diff)

    
    def status_handler(self, status, body, func, *func_args):
        inherited_arg = func_args[0]

        if status == 429:
            print("429")
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
            print("Sleeping 121s")
            sleep(121)
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

        print("A")
        self.queue_handler()
        r = requests.get(f"https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={self.API_key}")
        status = r.status_code
        body = r.json()
        
        return self.status_handler(status, body, self.get_ids_by_summoner_name, summoner_name)
        

a = API_calls("euw1", "europe", API_key)

for i in range(120):
    print(i, a.get_ids_by_summoner_name("Boeira")["name"])