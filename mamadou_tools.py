from pymongo import MongoClient
import pandas as pd
import json

client = MongoClient()
db = client["Projet_Bachelor"]

# DISTINCT
distinct_position = db.players.distinct("position")


# ------------------------ STATISTIQUE AGE ------------------------
def avg_players_age():
    under_40 = {"$match": {"age": {"$gt": 0, "$lt": 45}}}
    avg_age = {"$group": {"_id": "", "moyenne": {"$avg": "$age"}}}
    avg_age_under_40 = db.players.aggregate([under_40, avg_age])
    return int(list(avg_age_under_40)[0]["moyenne"])


def max_players_age():
    under_40 = {"$match": {"age": {"$gt": 0, "$lt": 45}}}
    max_age = {"$group": {"_id": "", "max": {"$max": "$age"}}}
    max_age_under_40 = db.players.aggregate([under_40, max_age])
    return int(list(max_age_under_40)[0]["max"])


def min_players_age():
    under_40 = {"$match": {"age": {"$gt": 0, "$lt": 45}}}
    min_age = {"$group": {"_id": "", "min": {"$min": "$age"}}}
    min_age_under_40 = db.players.aggregate([under_40, min_age])
    return int(list(min_age_under_40)[0]["min"])


# ------------------------ STATISTIQUE TAILLE ------------------------
def avg_players_height():
    group_height = {"$group": {"_id": "", "moyenne": {"$avg": "$height"}}}
    avg_height = db.players.aggregate([group_height])
    return int(list(avg_height)[0]["moyenne"])


def max_players_height():
    group_height = {"$group": {"_id": "", "max": {"$max": "$height"}}}
    max_height = db.players.aggregate([group_height])
    return int(list(max_height)[0]["max"])


def min_players_height():
    sup_nul = {"$match": {"height": {"$gt": 1}}}
    group_height = {"$group": {"_id": "", "min": {"$min": "$height"}}}
    min_height = db.players.aggregate([sup_nul, group_height])
    return int(list(min_height)[0]["min"])


# ------------------------ STATISTIQUE WEIGHT ------------------------
def avg_players_weight():
    group_weight = {"$group": {"_id": "", "moyenne": {"$avg": "$weight"}}}
    avg_weight = db.players.aggregate([group_weight])
    return int(list(avg_weight)[0]["moyenne"])


def max_players_weight():
    group_weight = {"$group": {"_id": "", "max": {"$max": "$weight"}}}
    max_weight = db.players.aggregate([group_weight])
    return int(list(max_weight)[0]["max"])


def min_players_weight():
    sup_nul = {"$match": {"weight": {"$gt": 1}}}
    group_weight = {"$group": {"_id": "", "min": {"$min": "$weight"}}}
    min_weight = db.players.aggregate([sup_nul, group_weight])
    return int(list(min_weight)[0]["min"])


def pl_groupby_position():
    group_position = {"$group":
                          {"_id": "$position",
                           "count": {"$sum": 1}
                           }}

    return list(db.players.aggregate([group_position]))

def df_player_by_position():
    player_by_position = pl_groupby_position()
    df_player_by_position = pd.DataFrame(player_by_position)

    df_player_by_position["new_position"] = " "
    df_player_by_position.loc[df_player_by_position['_id'].isin(["CB", "GK", "LB", "LWB", "RB", "RWB"]), "new_position"] = "DEFENSEUR"
    df_player_by_position.loc[df_player_by_position['_id'].isin(["CAM", "CDM", "CM", "RM"]), "new_position"] = "MILEU"
    df_player_by_position.loc[df_player_by_position['_id'].isin(["CF", "LF", "LM", "LW", "RF", "RW", "ST"]), "new_position"] = "ATTAQUANT"

    new_df = df_player_by_position.groupby("new_position")["count"].sum()
    new_df = new_df.reset_index()

    return new_df
