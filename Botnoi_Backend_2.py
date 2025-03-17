from collections import OrderedDict
import requests
from flask import Flask, request, Response
import json

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False

@app.route('/pokemon', methods=['POST'])
def get_pokemon_data():

    pokemon_id = 1

    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    pokemon_response = requests.get(pokemon_url)
    pokemon_data = pokemon_response.json() #stats 

    pokemon_form_url = f"https://pokeapi.co/api/v2/pokemon-form/{pokemon_id}/"
    pokemon_form_response = requests.get(pokemon_form_url)
    pokemon_form_data = pokemon_form_response.json() #name, prites

    stats = pokemon_data["stats"]
    name = pokemon_form_data["name"]
    prites = pokemon_form_data["sprites"]

    response = OrderedDict([
        ("stats", stats),  
        ("name", name),
        ("prites", prites)
    ])

    json_string = json.dumps(response, indent=4)
    return Response(json_string, content_type='application/json')
    #check curl -X POST http://127.0.0.1:5000/pokemon -H "Content-Type: application/json" -d "{}"
 
if __name__ == '__main__':
    app.run(debug=True)

#the output is always in name prites stat instead of stat name prites 
#I tried contruct json step by step 
#I tried ordereddict 
#I tried app.config["JSON_SORT_KEYS"] = False
#figure out the problem is with jsonify -> use json.dumps

