#coffee menu를 그대로 활용했다.
from flask import Flask, jsonify, request
flask_mission = Flask(__name__)
#자원
weapons = [
    {'id':0,'name':'missile','stock':1000}
    ]
    
# 여러분의 github id를 반환합니다.
@flask_mission.route('/whoami')
def get_id():
    return jsonify({"name" : "joseokjun"})
    
# Key와 Value
@flask_mission.route('/echo')
def get_string():
    string_value = request.args.get('string')
    return jsonify({"value" : string_value})

# Read
@flask_mission.route('/weapon')
def get_weapon():
    return jsonify(weapons)

# Create
@flask_mission.route('/weapon', methods=['POST'])
def create_weapon():
    request_data = request.get_json()
    
    new_weapon = {
        'id' : request_data['id'],
        'name' : request_data['name'],
        'stock' : request_data['stock']
        }
    
    weapons.append(new_weapon)
    return jsonify(new_weapon)

# Update
@flask_mission.route('/weapon/<int:id>', methods=['PUT'])
def update_weapons(id):
    request_data = request.get_json()
    update_weapon = {
        'id' : id,
        'name' : request_data['name'],
        'stock' : request_data['stock']
        }
    weapons[id] = update_weapon
    return jsonify(update_weapon)

# Delete
@flask_mission.route('/weapon/<int:id>', methods=['DELETE'])
def delete_weapon(id):
    del weapons[id]
    return jsonify(weapons)
    
if __name__ == '__main__':
    flask_mission.run()