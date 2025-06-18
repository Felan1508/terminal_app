from django.shortcuts import render

def room(request, room_name):
    return render(request, 'chatapp/room_selector.html', {
        'room_name': room_name
    })



def room_selector(request):
    rooms = ['room1', 'room2', 'room3', 'room4', 'room5']
    return render(request, 'chatapp/room_selector.html', {'rooms': rooms})