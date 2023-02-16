from pymongo import MongoClient
from operations import Operations
from datetime import timedelta
import yaml
from yaml.loader import BaseLoader

class MongoDbManagement:
    
    def __init__(self):
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=BaseLoader)
        self.operations = Operations()
        client = MongoClient(config['mongo_db_url'])
        self.db = client[config['mongo_db_collection_name']]
    
    def get_search_filters(self, parameters):
        """loop through parameters where keys are the column names and values are the values to be searched as the type list.
            prepare the filter dictionary to be used in the find method of pymongo. The format of the filter dictionary is {"column_name": {"$in": [value1, value2, value3]}} this way the find method will return all the documents that have the value1, value2, value3 in the column_name column.
            If value is string instead of list, then check if it has an operator in it. If "<" in the value, then use {"column_name": {"$lt": value}}. If ">" in the value, then use {"column_name": {"$gt": value}}. If "=" in the value, then use {"column_name": value}. If no operator in the value, then use {"column_name": value}
        """
        filter_dict = {}
        for key, value in parameters.items():
            if type(value) is list:
                filter_dict[key] = {"$in": value}
            elif type(value) is str:
                if "<" in value:
                    filter_dict[key] = {"$lt": value.replace("<", "").strip()}
                elif ">" in value:
                    filter_dict[key] = {"$gt": value.replace(">", "").strip()}
                else:
                    filter_dict[key] = value.replace("=", "").strip()
        
        return filter_dict
                
    
    def add_room(self, parameters):
        room_id = self.operations.generate_room_id(parameters['room_floor'],\
            parameters['room_number'], parameters['room_type'])
        
        # check if room already exists
        if self.db['room'].find_one({'room_id': room_id}) is not None:
            return False
        date_list = self.operations.genereate_seven_day()
        info_list = []
        parameters['room_id'] = room_id
        for date in date_list:
            info = {"date": date, "is_available": 0}
            info_list.append(info)
        parameters['info'] = info_list
        self.db['room'].insert_one(parameters)
        
        return room_id
    
    def delete_room(self, parameters):
        
        status = self.db['room'].delete_one({'room_id': parameters['room_id']})
        if status.deleted_count == 0:
            return False
        
        return parameters['room_id']

    def get_room_list(self, parameters):
        filters = self.get_search_filters(parameters)
        room_list = []
        for room in self.db['room'].find(filters, {'_id': 0}):
            room_list.append(room)
        
        return room_list
    
    def add_customer(self, parameters):
        
        last_cust_id = self.db['customer'].find_one(sort=[('customer_id', -1)])
        if last_cust_id is None:
            customer_id = 10000001
        else:
            customer_id = last_cust_id['customer_id'] + 1
        
        parameters['customer_id'] = customer_id
        self.db['customer'].insert_one(parameters)
        
        return customer_id
    
    def get_customer_list(self, parameters):
        filters = self.get_search_filters(parameters)
        
        customer_list = []
        
        for customer in self.db['customer'].find(filters, {'_id': 0}):
            customer_list.append(customer)
        
        return customer_list
        
    def add_reservation(self, parameters):
        
        # get each date from parameters[check_in_date] to parameters[check_out_date] as string
        date_range = self.operations.generate_dates_between_two_dates(parameters['check_in_date'], parameters['check_out_date'])
        filter_check_list = [{"date": date, "is_available": 0} for date in date_range]
        # check if room is available at the date ranges
        room_status = self.db['room'].find_one({"room_id": parameters['room_id'], "info": {"$all": filter_check_list}}, {"_id": 0})
        if room_status is None:
            return False

        # generate reservation id
        last_reservation_id = self.db['reservation'].find_one(sort=[('reservation_id', -1)])
        if last_reservation_id is None:
            reservation_id = 20000001
        else:
            reservation_id = last_reservation_id['reservation_id'] + 1
        
        parameters['reservation_id'] = reservation_id
        
        # self.db['room'].update_one({'room_id': parameters['room_id']}, {'$set': {'is_available': room_availability}})
        self.db['room'].update_one({"room_id": parameters["room_id"]}, {"$set": {"info.$[elem].is_available": 1}}, array_filters=[{"elem.date": {"$gte": parameters['check_in_date'], "$lte": parameters['check_out_date']}}])
        self.db['reservation'].insert_one(parameters)
        
        return reservation_id
    
    def delete_reservation(self, parameters):
        
        reservation = self.db['reservation'].find_one({'reservation_id': parameters['reservation_id']}, {'_id': 0})
        if reservation is None:
            return False # reservation not found

        room_info = self.db['room'].find_one({'room_id': reservation['room_id']}, {'_id': 0, 'is_available': 1})['is_available']
        
        check_in_date = self.operations.convert_string_to_date(reservation['check_in_date'])
        check_out_date = self.operations.convert_string_to_date(reservation['check_out_date'])
        number_of_reservation_day = self.operations.get_number_of_reservation_day(check_in_date, check_out_date)
        
        for i in range(number_of_reservation_day):
            date = str(check_in_date + timedelta(days=i))
            room_info[date] = 0
        
        self.db['room'].update_one({'room_id': reservation['room_id']}, {"$set": {'is_available': room_info}})
        self.db['reservation'].delete_one({'reservation_id': parameters['reservation_id']})
        
        return parameters['reservation_id']
    
    def get_reservation_list(self, parameters):
        filters = self.get_search_filters(parameters)
        
        reservation_list = []
        for reservation in self.db['reservation'].find(filters, {'_id': 0}):
            reservation_list.append(reservation)
        
        if len(reservation_list) == 0:
            return False
        return reservation_list
    
    def check_room_availability(self, parameters):
        
        available_date_list = []
        
        info_dict = self.db['room'].find_one({"room_id": parameters["room_id"]}, {"_id": 0, "info": 1})
        if info_dict is None:
            return False
        
        for info in info_dict['info']:
            if info['is_available'] == 0:
                available_date_list.append(info['date'])

        return available_date_list

    def get_available_room(self, parameters):
        
        date_range = self.operations.generate_dates_between_two_dates(parameters['check_in_date'], parameters['check_out_date'])
        filter_check_list = [{"date": date, "is_available": 0} for date in date_range]
        
        available_room_list = []
        for each in self.db['room'].find({"info": {"$all": filter_check_list}}, {"_id": 0, "info": 0}):
            available_room_list.append(each)
        
        if len(available_room_list) == 0:
            return False
        
        return available_room_list