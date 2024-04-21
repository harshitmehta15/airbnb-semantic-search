from openai import OpenAI
from dotenv import load_dotenv
import os
from pymongo import MongoClient
load_dotenv()
 
# Connecting to the Open AI Project 
client = OpenAI(
  organization='org-uiwVYwqC1ViLjnLfADyEJ4lQ',
  project='proj_I0hbaemhs3d7DztWfTWSYfgx',
  api_key=os.environ.get("OPENAI_API_KEY")
)

# Generating query embeddings with the text and model specified in the params
response = client.embeddings.create(
    input="romantic candle light",
    model="text-embedding-3-small"
)

# print(response.data[0].embedding) 

client = MongoClient(os.environ.get("MONGODB_URI"))
result = client['airbnb']['properties'].aggregate([
    {
        '$vectorSearch': {
            'queryVector': response.data[0].embedding, 
            'path': 'text_embeddings', 
            'numCandidates': 100, 
            'index': 'vector_index', 
            'limit': 100
        }
    }, {
        '$match': {
            'address.country': 'Turkey'
        }
    }, {
        '$project': {
            '_id': 0, 
            'listing_url': 1, 
            'property_type': 1, 
            'apartment_type': 1, 
            'name': 1, 
            'address.street': 1, 
            'description': 1, 
            'score': {
                '$meta': 'vectorSearchScore'
            }
        }
    }
])

#Priting results
for doc in result:
    print("Listing URL:", doc.get('listing_url'))
    print("Property Type:", doc.get('property_type'))
    print("Apartment Type:", doc.get('apartment_type'))
    print("Name:", doc.get('name'))
    print("Street Address:", doc.get('address', {}).get('street'))
    print("Description:", doc.get('description'))
    print("Score:", doc.get('score'))
    print()