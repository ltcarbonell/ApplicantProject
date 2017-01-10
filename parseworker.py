import os
import json
import csv
import xml.etree.ElementTree as ET
import sys

import workqueue

# Class definitions
class Agent(object):
    """Agent class"""
    name = ""
    agent_code = ""
    phone = ""
    city = ""
    state = ""
    zip = ""

    def __init__(self, agent_code, name, phone, city, state, zip):
        self.name = name
        self.agent_code = agent_code
        self.phone = phone
        self.city = city
        self.state = state
        self.zip = zip


def make_agent(agent_code, name = "", phone = "", city = "", state = "", zip = ""):
    agent = Agent(agent_code, name, phone, city, state, zip)
    return agent


class Office(object):
    """Office class"""
    name = ""
    office_code = ""
    phone = ""
    city = ""
    state = ""
    zip = ""

    def __init__(self, office_code, name, phone, city, state, zip):
        self.name = name
        self.office_code = office_code
        self.phone = phone
        self.city = city
        self.state = state
        self.zip = zip

def make_office(office_code, name = "", phone = "", city = "", state = "", zip = ""):
    office = Office(office_code, name, phone, city, state, zip)
    return office


class Listing(object):
    """Listing class for each propery"""
    address = ""
    city = ""
    state = ""
    zip = ""
    mls_number = ""
    price = ""
    status = ""
    type = ""
    description = ""
    agent = ""
    office = ""

    def __init__(self, address, city, state, zip, mls_number, price, status, type, description, agent, office):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.mls_number = mls_number
        self.price = price
        self.status = status
        self.type = type
        self.description = description
        self.agent = agent
        self.office = office

def make_listing(address, city, state, zip, mls_number, price, status, type, description, agent, office):
    listing = Listing(address, city, state, zip, mls_number, price, status, type, description, agent, office)
    return listing








# Functions defined

# Converts to strings
def strNoneCheck(value):
    # if it is already a string, return it
    if type(value) == str:
        return value
    # if value is None make it an empty string
    elif value is None:
        return ''
    # Convert value to string
    else:
        return str(value.text)

def parseXML(filename) :
    root = ET.parse(filename+".xml").getroot()
    # create arrays for parsed data to be added to
    listings = []
    offices = []
    agents = []
    for element in root.findall('listing'):
        # Data for listings
        address = strNoneCheck(element.find('address').find('street'))
        city = strNoneCheck(element.find('address').find('city'))
        state = strNoneCheck(element.find('address').find('state'))
        zip = strNoneCheck(element.find('address').find('zip'))
        mls_number = strNoneCheck(element.find('mls_number'))
        price = strNoneCheck(element.find('price'))
        status = strNoneCheck(element.find('status'))
        type = strNoneCheck(element.find('type'))
        description = strNoneCheck(element.find('description'))

        # Data for Agents
        agent_name = strNoneCheck(element.find('agent').find('name'))
        agent_code = strNoneCheck(element.find('agent').find('code'))
        agent_phone = strNoneCheck(element.find('agent').find('phone'))
        agent_city = strNoneCheck(element.find('agent').find('city'))
        agent_state = strNoneCheck(element.find('agent').find('state'))
        agent_zip = strNoneCheck(element.find('agent').find('zip'))

        # Data for Offices
        office_name = strNoneCheck(element.find('broker').find('name'))
        office_code = strNoneCheck(element.find('broker').find('code'))
        office_phone = strNoneCheck(element.find('broker').find('phone'))
        office_city = strNoneCheck(element.find('broker').find('city'))
        office_state = strNoneCheck(element.find('broker').find('state'))
        office_zip = strNoneCheck(element.find('broker').find('zip'))

        # Initialize the data sets
        agent = make_agent(agent_code, agent_name, agent_phone ,agent_city, agent_state, agent_zip)
        office = make_office(office_code, office_name, office_phone ,office_city, office_state, office_zip)
        listing = make_listing(address, city, state, zip, mls_number, price, status, type, description, agent, office)

        # Add data sets to arrays
        listings.append(listing)
        agents.append(agent)
        offices.append(office)

    # Call workqueue to save data
    workqueue.saveData(listings, agents, offices)
    print("Finished parsing "+filename)

def parseJSON(filename):
    json_data=open(filename+".json").read()
    data = json.loads(json_data)

    # create arrays for parsed data to be added to
    listings = []
    offices = []
    agents = []
    for item in data:
        address = item['street_address']
        city = item['city']
        state = item['state']
        zip = item['zip']
        mls_number = item['mls_number']
        price = item['price']
        status = item['status']
        type = item['type']
        description = item['description']

        agent_name = item['agent_name']
        agent_code = item['agent_code']
        agent_phone = item['agent_phone']


        office_name = item['office_name']
        office_code = item['office_code']
        office_phone = item['office_phone']

        # Initialize the data sets
        agent = make_agent(agent_code, agent_name, agent_phone,city, state, zip)
        office = make_office(office_code, office_name, office_phone,city, state, zip)
        listing = make_listing(address, city, state, zip, mls_number, price, status, type, description, agent, office)

        # Add data sets to arrays
        listings.append(listing)
        agents.append(agent)
        offices.append(office)

    # Call workqueue to save data
    workqueue.saveData(listings, agents, offices)
    print("Finished parsing "+filename)

def parseCSV(filename):
    # create arrays for parsed data to be added to
    listings = []
    offices = []
    agents = []
    # if "agent" in filename:
    file = open(filename+".csv")
    csv_data = csv.reader(file)
    rownum = 0
    header = ""
    for row in csv_data:
        if rownum == 0:
            header = row
        else:
            if "agent" in filename:
                # Save information for Agent
                agent_name = strNoneCheck(row[0])
                agent_code = strNoneCheck(row[1])
                agent_phone = strNoneCheck(row[3])
                agent_city = strNoneCheck(row[4])
                agent_state = strNoneCheck(row[5])
                agent_zip = strNoneCheck(row[6])
                agent = make_agent(agent_code, agent_name, agent_phone,agent_city, agent_state, agent_zip)
                agents.append(agent)
            elif "office" in filename:
                # Save information for Office
                office_name = strNoneCheck(row[0])
                office_code = strNoneCheck(row[1])
                office_phone = strNoneCheck(row[2])
                office_city = strNoneCheck(row[3])
                office_state = strNoneCheck(row[4])
                office_zip = strNoneCheck(row[5])
                office = make_office(office_code, office_name, office_phone,office_city, office_state, office_zip)
                offices.append(office)
            elif "listing" in filename:
                # Save information for Listing
                mls_number = strNoneCheck(row[0])
                address = strNoneCheck(row[1])
                city = strNoneCheck(row[2])
                state = strNoneCheck(row[3])
                zip = strNoneCheck(row[4])
                price = strNoneCheck(row[5])
                status = strNoneCheck(row[6])
                type = strNoneCheck(row[7])
                agent = make_agent(agent_code = strNoneCheck(row[8]))
                office = make_office(office_code = strNoneCheck(row[9]))
                description = strNoneCheck(row[10])
                listing = make_listing(address, city, state, zip, mls_number, price, status, type, description, agent, office)
                listings.append(listing)
        rownum += 1

    # Call workqueue to save data
    workqueue.saveData(listings, agents, offices)
    print("Finished parsing "+filename)

def parseFile(file):
    filename, file_extension = os.path.splitext(file)

    if file_extension == '.xml':
        parseXML(filename)
    elif file_extension == '.json':
        parseJSON(filename)
    elif file_extension == '.csv':
        parseCSV(filename)

# Main Method
def main():
    if len(sys.argv) == 2:
        parseFile(sys.argv[1])
    else:
        print("incorrect number of arguments")

# Make sure only this script can call the main function
if __name__ == '__main__':
    main()
