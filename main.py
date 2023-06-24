# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json

# Request data
data = {'key': 'value'}

# Convert data to JSON
json_data = json.dumps(data)

# auth_key
X_Auth_Token = '5e9befb6a945932c4831bd1541c61fb6'

Authorization = ''

base_url = 'https://7zszxecwra.execute-api.ap-northeast-2.amazonaws.com/api/'

problem = 1

lastDay = 200 if problem == 1 else 1000
height = 3 if problem == 1 else 10
roomsOF = 20 if problem == 1 else 200
maxAmount = 10 if problem == 1 else 50

hotel = [[[] for _ in range(roomsOF + 1)] for _ in range(height + 1)]

# Set the headers

headersForStart = {"Content-Type": "application/json", "X-Auth-Token": X_Auth_Token}

startRequestBody = {"problem": problem}

# Send the POST request with JSON data
response = requests.post(base_url + 'start', headers=headersForStart, data=json.dumps(startRequestBody))

# Check the response status code
if response.status_code != 200:
    print('failed to start. check X_Auth_Token')
    exit()

start_response = response.json()
Authorization = start_response['auth_key']

headers = {'Content-Type': 'application/json', 'Authorization': Authorization}

check_in_clients = [[] for _ in range(lastDay + 1)]
check_out_clients = [[] for _ in range(lastDay + 1)]


def clear(day):
    for client in check_out_clients[day]:
        floor = int(client['room_number'] / 1000)
        startingroom = client['room_number'] % 1000
        for roomof in range(startingroom, startingroom + client['reservation_info']['amount']):
            hotel[floor][roomof].remove(client['reservation_info'])


def checkAvailability(reserverequest):
    for floor in range(1, height + 1):
        contiguous = 0
        for roomOF in range(1, roomsOF + 1):
            if checkAvailabilityForARoom(floor, roomOF, reserverequest):
                contiguous += 1
                if contiguous == reserverequest['amount']:
                    return (floor * 1000) + roomOF - reserverequest['amount'] + 1
            else:
                contiguous = 0
    return -1


# hotel = [[None for _ in range(3)] for _ in range(4)]
def checkAvailabilityForARoom(floor, roomof, reserverequest):
    check_in_date = reserverequest['check_in_date']
    check_out_date = reserverequest['check_out_date']
    if len(hotel[floor][roomof]) == 0:
        return True
    if hotel[floor][roomof][0]['check_in_date'] >= check_out_date:
        return True
    for idx in range(1, len(hotel[floor][roomof])):
        if hotel[floor][roomof][idx - 1]['check_out_date'] <= check_in_date and hotel[floor][roomof][idx][
            'check_in_date'] >= check_out_date:
            return True
    if hotel[floor][roomof][len(hotel[floor][roomof]) - 1]['check_out_date'] <= check_in_date:
        return True
    return False


def assignRooms(roomNumber, reservation_info):
    floor = int(roomNumber / 1000)
    roomof = roomNumber % 1000
    check_in_date = reservation_info['check_in_date']
    check_out_date = reservation_info['check_out_date']
    check_in_clients[check_in_date].append({'id': reservation_info['id'], 'room_number': roomNumber})
    check_out_clients[check_out_date].append({'room_number': roomNumber, 'reservation_info': reservation_info})
    for room in range(roomof, roomof + reservation_info['amount']):
        assignARoom(floor, room, reservation_info, check_in_date, check_out_date)  # room이 아닌 roomof였음


def assignARoom(floor, roomof, reservation_info, check_in_date, check_out_date):
    if len(hotel[floor][roomof]) == 0:
        hotel[floor][roomof].append(reservation_info)
        return
    if hotel[floor][roomof][0]['check_in_date'] >= check_out_date:
        hotel[floor][roomof].insert(0, reservation_info)
        return
    for idx in range(1, len(hotel[floor][roomof])):
        if hotel[floor][roomof][idx - 1]['check_out_date'] <= check_in_date and hotel[floor][roomof][idx][
            'check_in_date'] >= check_out_date:
            hotel[floor][roomof].insert(idx, reservation_info)
            return
    hotel[floor][roomof].append(reservation_info)


def reply(replies):
    requests.put(base_url + 'reply', headers=headers, data=json.dumps({'replies': replies}))


def simulate(room_assign):
    hello = requests.put(base_url + 'simulate', headers=headers, data=room_assign).json()
    if hello['fail_count'] > 0:
        print(hello['fail_count'])


def score():
    print(requests.get(base_url + 'score', headers=headers).text)


for day in range(1, lastDay + 1):
    clear(day)
    print('day ' + str(day))
    reservRequests = requests.get(base_url + 'new_requests', headers=headers).json()['reservations_info']
    if len(reservRequests) > 0:
        replies = []
        for reservRequest in reservRequests:
            roomNumber = checkAvailability(reservRequest)  # either serve
            if roomNumber == -1:
                replies.append({'id': reservRequest['id'], 'reply': 'refused'})
                continue
            assignRooms(roomNumber, reservRequest)
            replies.append({'id': reservRequest['id'], 'reply': 'accepted'})
        reply(replies)
    room_assign = []
    if len(check_in_clients[day]) != 0:
        for client in check_in_clients[day]:
            room_assign.append(client)
    simulate(json.dumps({'room_assign': room_assign}))
score()
