from flask import Flask, request
import yaml
from yaml.loader import BaseLoader
from mongo_db_management import MongoDbManagement

# db = JsonDbManagement()
db = MongoDbManagement()

app = Flask(__name__)
with open('config.yaml') as f:
    config = yaml.load(f, Loader=BaseLoader)


def read_input(operation, input_file):
    if operation == 'add_room':
        return input_file if 'room_type' and 'room_floor' and 'room_number' \
            in input_file else None
            
    elif operation == 'delete_room':
        return input_file if 'room_id' in input_file else None
        
    elif operation == 'get_room_list':
        return input_file
            
    elif operation == 'add_customer':
        return input_file if 'first_name' and 'last_name' and 'email' \
            and 'phone_number' and 'date_of_birth' in input_file else None

    elif operation == 'get_customer_list':
        return input_file
            
    elif operation == 'add_reservation':
        return input_file if 'customer_id' and 'room_id' and 'check_in_date' \
            and 'check_out_date' in input_file else None
                
    elif operation == 'delete_reservation':
        return input_file if 'reservation_id' in input_file else None
    
    elif operation == 'get_reservation_list':
        return input_file
    
    elif operation == 'check_room_availability':
        return input_file if 'room_id' in input_file else None

    elif operation == 'get_available_room':
        return input_file if 'check_in_date' and 'check_out_date' \
            in input_file else None

    else:
        return None
    
    
@app.route('/add_room', methods=['POST'])
def add_room():
    
    input_file = request.get_json()
    
    input_parameters = read_input('add_room', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    room_id = db.add_room(input_parameters)
    if room_id is False:
        return config['room_already_exists']
    
    result = {'satutus': 'success', 'message': f'room added successfully with room id {room_id}'}
    return result
    
    
@app.route('/delete_room', methods=['POST'])
def delete_room():
    input_file = request.get_json()
    
    input_parameters = read_input('delete_room', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    room_id = db.delete_room(input_parameters)
    if room_id is False:
        return config['room_not_found']
    
    result = {'satutus': 'success', 'message': f'room deleted successfully with room id {room_id}'}
    return result


@app.route('/get_room_list', methods=['POST'])
def get_room_list():
    input_file = request.get_json()
    
    input_parameters = read_input('get_room_list', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    room_list = db.get_room_list(input_file)
    if room_list is False:
        return config['no_room_found']
    
    result = {'satutus': 'success', 'room_list': room_list}
    return result


@app.route('/add_customer', methods=['POST'])
def add_customer():
    # parameters: firstname, lastname, email, phone_number, date_of_birth
    input_file = request.get_json()
    
    input_parameters = read_input('add_customer', input_file)
    if input_parameters is None:
        return config['invalid_input']

    customer_id = db.add_customer(input_parameters)
    
    result = {'satutus': 'success', 'message': f'Customer is added with customer_id: {customer_id}'}
    return result

@app.route('/get_customer_list', methods=['POST'])
def get_customer_list():
    # parameters: firstname, lastname, email, phone_number, date_of_birth
    input_file = request.get_json()
    
    input_parameters = read_input('get_customer_list', input_file)
    if input_parameters is None:
        return config['invalid_input']

    customer_id = db.get_customer_list(input_file)
    
    result = {'satutus': 'success', 'customer_list':customer_id}
    return result

@app.route('/add_reservation', methods=['POST'])
def add_reservation():
    input_file = request.get_json()
    
    input_parameters = read_input('add_reservation', input_file)
    if input_parameters is None:
        return config['invalid_input']

    reservation_id = db.add_reservation(input_parameters)
    if reservation_id is False:
        return config['room_not_available']
    
    result = {'satutus': 'success', 'message': f'Reservation is added with reservation_id: {reservation_id}'}
    return result


@app.route('/delete_reservation', methods=['POST'])
def delete_reservation():
    input_file = request.get_json()
    
    input_parameters = read_input('delete_reservation', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    reservation_id = db.delete_reservation(input_parameters)
    if reservation_id is False:
        return config['reservation_not_found']
    
    result = {'satutus': 'success', 'message': f'Reservation is deleted with reservation_id: {reservation_id}'}
    return result


@app.route('/get_reservation_list', methods=['POST'])
def get_reservation_list():
    input_file = request.get_json()
    
    input_parameters = read_input('get_reservation_list', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    reservation_list = db.get_reservation_list(input_parameters)
    if reservation_list is False:
        return config['reservation_not_found']
    
    reservation_list = {'satutus': 'success', 'reservation_list': reservation_list}
    return reservation_list


@app.route('/check_room_availability', methods=['POST'])    
def check_room_availability():
    """take input as room_id and return list of available dates"""
    input_file = request.get_json()
    
    input_parameters = read_input('check_room_availability', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    available_dates = db.check_room_availability(input_parameters)
    if available_dates is False:
        return config['room_not_found']
    
    result = {'satutus': 'success', 'available_dates': available_dates}
    return result
    
    
@app.route('/get_available_room', methods=['POST'])
def get_available_room():
    """take input as check_in_date, check_out_date
        return room attributes as dictionary"""
    
    input_file = request.get_json()
    
    input_parameters = read_input('get_available_room', input_file)
    if input_parameters is None:
        return config['invalid_input']
    
    available_rooms = db.get_available_room(input_parameters)
    if available_rooms is False:
        return config['no_room_available']
    
    result = {'satutus': 'success', 'available_rooms': available_rooms}
    return result
    
    
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=config['port'])