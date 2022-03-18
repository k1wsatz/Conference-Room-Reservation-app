import datetime

from django.shortcuts import render, redirect

# Create your views here.
from .models import ConferenceRoom, Reservation
from django.views import View


class AddConferenceRoom(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        alcohol = request.POST.get("alcohol") == "on"

        if not name:
            return render(request, "add_room.html", context={"error": "Please, provide room name!"})

        if capacity <= 0:
            return render(request, "add_room.html", context={"error": "Please, provide positive room capacity!"})

        if ConferenceRoom.objects.filter(name=name).first():
            return render(request, "add_room.html", context={"error": "Room with this name already exists!"})

        ConferenceRoom.objects.create(name=name, capacity=capacity, alcohol=alcohol)
        return redirect("room-list")


class ConferenceRoomListView(View):
    def get(self, request):
        rooms = ConferenceRoom.objects.all()
        return render(request, "room_list.html", context={"rooms": rooms})


class DeleteConferenceRoom(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        room.delete()
        return redirect("room-list")


class ModifyConferenceRoom(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        return render(request, "modify_room.html", context={"room": room})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        alcohol = request.POST.get("alcohol") == "on"

        if not name:
            return render(request, "modify_room.html", context={"error": "Please, provide room name!"})

        if capacity <= 0:
            return render(request, "modify_room.html", context={"error": "Please, provide positive room capacity!"})

        if ConferenceRoom.objects.filter(name=name).first():
            return render(request, "modify_room.html", context={"error": "Room with this name already exists!"})

        room.name = name
        room.capacity = capacity
        room.alcohol = alcohol
        room.save()
        return redirect("room-list")


class ReservationView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, "reservations.html", context={"room": room, "reservations": reservations})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        date = request.POST.get('reservation-date')
        comment = request.POST.get('comment')

        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')

        if Reservation.objects.filter(room_id=room, date=date):
            return render(request, "reservations.html", context={"roon": room,
                                                                 "reservations": reservations,
                                                                 "error": "The room has already been booked!"})
        if date < str(datetime.date.today()):
            return render(request, "reservations.html", context={"room": room,
                                                                 "reservations": reservations,
                                                                 "error": "This is a past date!"})

        Reservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("room-list")


class DetailView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, "room_details.html", context={"room": room, "reservations": reservations})


class SearchView(View):
    def get(self, request):
        name = request.GET.get("room-name")
        capacity = request.GET.get("capacity")
        capacity = int(capacity) if capacity else 0
        alcohol = request.GET.get("projector") == "on"

        rooms = ConferenceRoom.objects.all()
        if alcohol:
            rooms = rooms.filter(alcohol=alcohol)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = str(datetime.date.today()) in reservation_dates

        return render(request, "room_list.html", context={"rooms": rooms, "date": datetime.date.today()})