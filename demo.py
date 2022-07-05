from API_requests import *
from scripts import *
import pyperclip

file = open("API_keys.txt", "r")
API_key = file.readlines()[0]
file.close()

rec_depth = 0
def find_path(start_ids, end_ids, API_key):
    cons = API_calls("euw1", "europe", API_key)
    initial_match_hist = cons.get_matches_by_puuid(start_ids["puuid"])
    initial_losers = cons.get_loser_ids_from_match_ids(initial_match_hist, start_ids)


    def dfs(visited, graph, node):
        global rec_depth

        cons = API_calls("euw1", "europe", API_key)

        if node not in visited and node != end_ids["puuid"]:
            rec_depth += 1
            node_ids = cons.get_ids_by_puuid(node)
            
            visited.add(node)
            visited2.add(node)
            
            defender_stats = cons.get_summoner_stats_by_id(node_ids["id"])
            defender_rank = str_rank_to_int(defender_stats["league"], defender_stats["division"], defender_stats["league_points"])

        
            for match in graph[node]:
                key = list(match.keys())[0]
                for player_ids in match[key]:
                    neighbour = player_ids["puuid"]
                    visited2.add(neighbour)

                    match_list = cons.get_matches_by_puuid(neighbour)
                    graph[neighbour] = cons.get_loser_ids_from_match_ids(match_list, player_ids)

                    chall_stats = cons.get_summoner_stats_by_id(player_ids["summoner_id"])
                    chall_rank = str_rank_to_int(chall_stats["league"], chall_stats["division"], chall_stats["league_points"])
                    print(node_ids["summoner_name"] + " vs " + player_ids["summoner_name"])
                    print(str(defender_rank) + " vs " + str(chall_rank))
                    print("LEN STACK: " + str(len(visited)))
                    print("LEN VISITED: " + str(len(visited2)))
                    print("REC DEPTH: " + str(rec_depth))
                    print()

                    if chall_rank >= defender_rank:
                        dfs(visited, graph, neighbour)

            rec_depth -= 1



    # deprecated - enters infinite loop when backtracking
    def iterative_dfs(graph, node):
        visited = set()
        stack = [node]
        chall_fail = set()
        while stack:
            node = stack[-1]
            if node not in visited and node != end_ids["puuid"]:
                visited.add(node)

            node_ids = cons.get_ids_by_puuid(node)
            defender_stats = cons.get_summoner_stats_by_id(node_ids["id"])
            defender_rank = str_rank_to_int(defender_stats["league"], defender_stats["division"], defender_stats["league_points"])

            remove_from_stack = True
            for match in graph[node]:

                print("Visiting: " + node_ids["summoner_name"] + " | Rank: " + str(defender_rank))
                print("LEN VISITED: " + str(len(visited)))
                print("LEN STACK: " + str(len(stack)))
                print("LEN FAILS: " + str(len(chall_fail)))
                print()

                key = list(match.keys())[0]
                for player_ids in match[key]:

                    neighbour = player_ids["puuid"]
                    visited.add(neighbour)

                    match_list = cons.get_matches_by_puuid(neighbour)
                    graph[neighbour] = cons.get_loser_ids_from_match_ids(match_list, player_ids)

                    chall_stats = cons.get_summoner_stats_by_id(player_ids["summoner_id"])
                    chall_rank = str_rank_to_int(chall_stats["league"], chall_stats["division"], chall_stats["league_points"])
                    print("Challenged by: " + player_ids["summoner_name"] + " | Rank: " + str(chall_rank))

                    if chall_rank >= defender_rank:
                        stack.append(neighbour)
                        remove_from_stack = False
                        break

                    else:
                        chall_fail.add(neighbour)
            
            if remove_from_stack:
                stack.pop()

        return stack

    visited = set()
    visited2 = set()
    graph = {start_ids["puuid"]: initial_losers}
    dfs(visited, graph, start_ids["puuid"])

    return visited, graph

x, y = find_path(API_calls("euw1", "europe", API_key).get_ids_by_summoner_name("Boeira"),
            API_calls("euw1", "europe", API_key).get_ids_by_summoner_name("MagiFelix5"),
            API_key)
    





