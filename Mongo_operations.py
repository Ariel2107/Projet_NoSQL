from pymongo import MongoClient
import statistics

client = MongoClient()
db = client["Projet_Bachelor"]
players_not_gk = {"$match": {"position": {"$ne": "GK"}}}
mean_ratings = {"$group":
                    {"_id": "",
                     "mean_rating": {"$avg": "$rating"},
                     "mean_pace": {"$avg": "$pace"},
                     "mean_shooting": {"$avg": "$shooting"},
                     "mean_passing": {"$avg": "$passing"},
                     "mean_dribbling": {"$avg": "$dribbling"},
                     "mean_defending": {"$avg": "$defending"},
                     "mean_physicality": {"$avg": "$physicality"},
                     }
                }
true_mean = {"$group":
                 {"_id": "",
                  "given_mean": {"$avg": "$rating"}
                  }
             }

given_moy = list(db.players.aggregate([true_mean]))[0]['given_mean']
print(given_moy)
sort = {'$sort': {'uniqueCount': -1}}
limitation = {'$limit': 100}
unique = {"$group": {"_id": "$name", "uniqueCount": {"$max": "$rating"}}}
l = list(db.players.aggregate([unique, sort, limitation]))
players_list = [i['_id'] for i in l]

# Calculating moyenne des attributs
# Every moyennes
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
