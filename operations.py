from datetime import datetime, timedelta, date

"""
This module contains the operations class which is used to perform the operations, 
"""

class Operations:
    
    
    def generate_room_id(self, room_floor, room_number, room_type):
        # XXXYYYYZ where is the XXX is the room_floor and YYYY is the room_number and Z is the room_type
        room_floor_zero_padding = self.return_number_with_zero_padding(room_floor, 3)
        room_number_zero_padding = self.return_number_with_zero_padding(room_number, 4)
        room_id =  room_floor_zero_padding + room_number_zero_padding + str(room_type)
        return room_id
    
    def return_number_with_zero_padding(self, number, digit):
        # compute the number of zeros to be padded
        number_of_zeros = digit - len(str(number))
        return number_of_zeros * "0" + str(number)
    
    def convert_string_to_date(self, date_string):
        # convert string to date
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    
    def get_number_of_reservation_day(self, end_date, start_date):
        # get number of days between two datetime objects
        range = (end_date - start_date).days
        return abs(range) + 1
    
    def genereate_seven_day(self):
        date_list = []
        today = date.today()
        for i in range(7):
            available_date = today + timedelta(days=i)
            date_list.append(str(available_date))
        return date_list

    def generate_dates_between_two_dates(self, start_date_str, end_date_str):
        date_list = []
        s_date = self.convert_string_to_date(start_date_str)
        e_date = self.convert_string_to_date(end_date_str)
        while s_date <= e_date:
            date_list.append(str(s_date))
            s_date += timedelta(days=1)
        
        return date_list
    