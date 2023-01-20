import pymongo

# Create the client
client = pymongo.MongoClient('localhost', 27017)

# Connect to our database
db = client['spin_chat_game']
players_collection = db['players']
games_collection = db['games']
