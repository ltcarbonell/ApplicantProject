import os
import shelve

def saveData(listings, agents, offices):
    # open the parsedData db (create if necessary)
    s = shelve.open("parsedData", "c")
    try:
        # check to see if each of the keys is alreay created
        # if so, add data to that key's values
        # if not create a new one and save it locally
        if s.has_key("listings"):
            s["listings"] += listings
        else:
            s["listings"] = listings

        if s.has_key("agents"):
            s["agents"] += agents
        else:
            s["agents"] = agents

        if s.has_key("offices"):
            s["offices"] += offices
        else:
            s["offices"] = offices
    finally:
        s.close()

def readData():
    listings = []
    agents = []
    offices = []
    # read the data from the parsedData db
    s = shelve.open("parsedData", "r")
    try:
        # get the data from the keys
        listings = s["listings"]
        agents = s["agents"]
        offices = s["offices"]
    finally:
        s.close()
    # return the arrays of listings, agents and offices
    return listings, agents, offices

def deleteFiles():
    # remove local db once done with it
    os.remove("parsedData.db")
