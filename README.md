# hotel-reservation-system-mongodb
A hotel reservation API developed with Flask.
The API has different endpoints for different tasks.
This program is developed for learning Mongodb.


## Endpoints

- /add_room
- /delete_room
- /get_room_list
- /add_customer
- /get_customer_list
- /add_reservation
- /delete_reservation
- /get_reservation_list
- /check_room_availability
- /get_available_room

## Filtering
```
Filters can be applied on */get_room_list, /get_customer_list, /get_reservation_list.*
Filters are optional and can be applied to any field of the fields.
Filters are taken from the user as JSON file with a POST operation.
For filtering by multiple values following input can be used: 
{
    "room_type": [0, 1, 2]
}
Any room with room type 0, 1 or 2 will be returned if the filter above sent to */get_room_list*

">", "<" or "=" can be applied to string values for filtering by values of the numbers, including dates.
{
	"date_of_birth": "< 2000-01-01"
}
Filter would return customers who has born before the year 2000 on the */get_customer_list*
```

## Endpoint input-output examples

### /add_room
```
input:
{
	"room_type":0,
	"room_floor":1,
	"room_number":1
}
output:
{
	"message": "room added successfully with room id 00200100",
	"satutus": "success"
}
```
### /delete_room
```
input:
{
	"room_id": "00100010"
}
output:
{
	"message": "room deleted successfully with room id 00100010",
	"satutus": "success"
}
```
### /add_customer
```
input:
{
	"first_name": "Mark",
	"last_name": "Josh",
	"email": "mjosh@mail.com",
	"phone": "2233445566",
	"date_of_birth": "1986-04-27"
}
```
### /add_reservation
```
input:
{
	"customer_id": 10000001,
	"room_id": "00100010",
	"check_in_date": "2023-02-07",
	"check_out_date": "2023-02-09"
}
```

### /check_room_availability
```
Returns the list of dates that the given room is available.
input:
{
	"room_id": "00100011"
}

output:
{
	"available_dates": [
		"2023-02-07",
		"2023-02-08",
		"2023-02-09",
		"2023-02-10",
		"2023-02-11",
		"2023-02-12",
		"2023-02-13"
	],
	"satutus": "success"
}
```
### /get_available_room
```
Returns room informations that are available in the date range given.
input:
{
	"check_in_date": "2023-02-10",
	"check_out_date": "2023-02-10"
}

output:
{
	"available_rooms": [
		{
			"room_floor": 1,
			"room_id": "00100011",
			"room_number": 1,
			"room_type": 1
		}
	],
	"satutus": "success"
}
```
