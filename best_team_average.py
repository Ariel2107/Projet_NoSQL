from pymongo import MongoClient

client = MongoClient()


db = client["Project_Bachelor"]
print("FIFA TEAM")
sort = {'$sort': {'rating': -1}}
position_wanted = ["GK", "CB", "RB", "LB", "CM", "CAM", "RW", "LW", "ST"]
projection = {"$project": {
    "_id": 0,
    "name": 1,
    "rating": 1,
    "moyenne aggrégée": {"$divide": [{"$add": ["$physicality", "$passing", "$dribbling", "$pace", "$shooting", "$defending"]}, 6]},
    }
}

for position in position_wanted:
    if position in ["CB", "CM"]:
        limitation = {'$limit': 2}
    else:
        limitation = {'$limit': 1}
    find_post = {"$match": {"position": position}}
    players = list(db.players.aggregate([find_post, projection, sort, limitation]))
    for player in players:
        print(f"{position}: {player['name']} {player['rating']} {player['moyenne aggrégée']}")

print("\nAGGREGATED TEAM\n")

sort = {"$sort": {'moyenne aggrégée': -1}}
for position in position_wanted:
    if position in ["CB", "CM"]:
        limitation = {'$limit': 2}
    else:
        limitation = {'$limit': 1}
    find_post = {"$match": {"position": position}}
    players = list(db.players.aggregate([find_post, projection, sort, limitation]))
    for player in players:
        print(f"{position}: {player['name']} {player['rating']} {player['moyenne aggrégée']}")