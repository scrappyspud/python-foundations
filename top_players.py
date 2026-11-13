import json

with open("players.json") as f:
    players = json.load(f)

top3 = sorted(players, key=lambda player:player["score"] , reverse=True)[:3]
with open("top3.json", "w") as f:
    json.dump(top3, f, indent=2)

ranks = enumerate(top3)

for rank in ranks:
    print(f"{rank[0] + 1}. {rank[1]["name"]} - {rank[1]["score"]}")

print(list(range(1_000_000_000)))