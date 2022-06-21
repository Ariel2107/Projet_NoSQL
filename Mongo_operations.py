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
ratings = list(db.players.find({}, {"pace": 1, "shooting": 1, "passing": 1, "dribbling": 1, "defending": 1,
                                    "physicality": 1, '_id': 0}))
ratings_values = []
for items in ratings:
    for key in items:
        ratings_values.append(items[key])
ratings_moy = statistics.mean(ratings_values)

# Every moyennes
match_player = {"$match": {"name": "Kylian Mbappé"}}
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

ratings_list = [values for key, values in list(db.players.aggregate([match_player, mean_ratings]))[0].items()][1:]
print(list(dict.keys(list(db.players.aggregate([match_player, mean_ratings]))[0]))[1:])

