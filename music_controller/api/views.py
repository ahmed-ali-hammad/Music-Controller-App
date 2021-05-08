from rest_framework import generics
from rest_framework import status
from .models import *
from .serializers import *


class RoomAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomRetrieveApiView(APIView):

    def get(self, request, code):
        queryset = Room.objects.filter (code = code)
        if queryset.count() == 1:
            serializer = RoomSerializer(queryset[0])
            data = serializer.data
            if data["host"] == self.request.session.session_key:
                data["is_host"] = True
            else:
                data["is_host"] = False
            return Response (data)
        else:
            return Response ("Code provided is't correct", status = status.HTTP_404_NOT_FOUND)


class RoomCreateAPIView(APIView):
    serializer_class = RoomCreateSerializer

    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = RoomCreateSerializer(data = request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.validated_data['guest_can_pause']
            votes_to_skip = serializer.validated_data['votes_to_skip']
            host = self.request.session.session_key
            queryset = Room.objects.filter(host = host)
            self.request.session["room_code"] = code
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields = ["guest_can_pause", "votes_to_skip" ])
            else:
                serializer.validated_data['host'] = host
                serializer.save()
            self.request.session["room_code"] = Room.objects.filter(host = host)[0].code
            return Response (RoomSerializer(Room.objects.filter(host = host)[0]).data)
        return Response (serializer.data)

class RoomJoinAPIView(APIView):
    def post(self, request):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        if 'code' in request.data:            
            code = request.data["code"]
            filter_results = Room.objects.filter(code = code)
            if filter_results.count() == 1:
                self.request.session["room_code"] = code
                return Response ({'message' : "Room Joined"}, status = status.HTTP_200_OK)
        return Response ({'Bad Request': 'Invalid Room Code'}, status = status.HTTP_400_BAD_REQUEST)

class UserInRoomAPIView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {'code': self.request.session.get('room_code')}
        return Response(data)

class LeaveRoomAPIView(APIView):
    def post(self, request):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host = host_id)
            if room_results.count ==1:
                room = room_results[0]
                room.delete()
        return Response ({'message': "success"})
