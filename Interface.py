#!/usr/bin/python2.7
#
# Assignment5 Interface
# Name: Suhas Venkatesh Murthy
#

from pymongo import MongoClient
import os
import sys
import json
import math
import re


def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):

    cityRows = collection.find({"city": re.compile(cityToSearch,re.IGNORECASE)})

    with open(saveLocation1,"w") as fl:
        for row in cityRows:
            fl.write(row["name"].encode('utf-8').upper()+ "$" +
                     row["full_address"].encode('utf-8').upper() +"$"
                     + row["city"].encode('utf-8').upper()+ "$"
                     + row["state"].encode('utf-8').upper())
            fl.write("\n")


def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    allRows = collection.find()
    latitude = float(myLocation[0])
    longitude = float(myLocation[1])
    business = []

    for row in allRows:
        categories = row["categories"]
        distancebtw = compute_distance(float(row["latitude"]), float(row["longitude"]), latitude, longitude)

        if distancebtw<=maxDistance:
            if len(list(set(categories) & set(categoriesToSearch))) != 0:
                business.append(row["name"].encode('utf-8').upper())

    with open(saveLocation2,"w") as fl:
        for i in range(0,len(business)):
            fl.write(business[i])
            fl.write("\n")


def compute_distance(lat2, lon2, lat1, lon1):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(float(delta_phi / 2)) * math.sin(float(delta_phi / 2)) + math.cos(phi1) * math.cos(phi2) * \
            math.sin(float(delta_lambda / 2)) * math.sin(float(delta_lambda / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return 3959 * c

