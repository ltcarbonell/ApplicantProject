import sqlite3
from parseworker import Listing, Agent, Office

import workqueue as wq

# Read arrays from files created by workqueue
listings, agents, offices = wq.readData()

# Connect to database
conn = sqlite3.connect('data/homes.com/homes.db')
c = conn.cursor()

#insert agents into table
for agent in agents:
    # check to see if that agent was already inserted
    c.execute('SELECT count(agent_code) FROM agents WHERE agent_code=?', (agent.agent_code,))
    if c.fetchone()[0] < 1:
        # if agent wasn't already inserted, insert into agents table
        c.execute("INSERT OR IGNORE INTO agents (name, agent_code, phone, city, state, zip) values (?,?,?,?,?,?)",(agent.name, agent.agent_code, agent.phone, agent.city, agent.state, agent.zip))

#insert offices into table
for office in offices:
    # check to see if that agent was already inserted
    c.execute('SELECT count(office_code) FROM offices WHERE office_code=?', (office.office_code,))
    if c.fetchone()[0] < 1:
        # if office wasn't already inserted, insert into offices table
        c.execute("INSERT OR IGNORE INTO offices (name, office_code, phone, city, state, zip) values (?,?,?,?,?,?)",(office.name, office.office_code, office.phone, office.city, office.state, office.zip))

#insert listings into table
for listing in listings:
    # check to see if that listings was already inserted
    c.execute("SELECT count(id) FROM listings "
    "WHERE address=? AND city=? AND state=? AND zip=? AND "
    "mls_number=? AND price=? AND status=? AND type=? AND "
    "description=?", (listing.address, listing.city, listing.state, listing.zip, listing.mls_number, listing.price, listing.status, listing.type, listing.description))
    if c.fetchone()[0] < 1:
        # if office wasn't already inserted, insert into offices table
        c.execute("INSERT INTO listings (address, city, state, zip, mls_number, price, status, type, description, agent_id, office_id) "
        "values (?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "(select id FROM agents "
        "WHERE agent_code = ?), "  # check for the correct agent id
        "(SELECT id FROM offices "
        "WHERE office_code = ?)" # check for the correct office id
        ")", (listing.address, listing.city, listing.state, listing.zip, listing.mls_number, listing.price, listing.status, listing.type, listing.description, listing.agent.agent_code, listing.office.office_code))

# make changes to database
conn.commit()
print("Database updated")
# close connection to database
conn.close()
# remove the temporary files created to store parsed data
wq.deleteFiles()
