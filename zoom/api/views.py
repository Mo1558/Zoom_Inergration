from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializer import MeetingSerializer
from zoom.models import Zoom
from zoom.ZoomClass import Meeting

class Meetings(APIView):
    '''
    this class to get all meeting from database
    '''
    def get(self, request):
        '''
        this method will get all meeting from database
        '''
        all_data = Zoom.objects.all()
        serializer = MeetingSerializer(all_data, many=True)
        return Response(serializer.data)

    

class CreateMeeting(APIView):
    '''
    this class is used to create a new meeting object
    '''
    def post(self, request):
        '''
        this method to create meeting and store his 
        information to database and return the data 
        '''
        create_meeting=Meeting().create_meeting()
     
        request.data['meeting_id']=create_meeting ["id"]
        request.data['created_by']=create_meeting ["host_email"]
        request.data['meeting_link']=create_meeting["join_url"]
        request.data['password']=create_meeting ["password"]

        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MeetingtDetail(APIView):
    '''
    this class to get , update and delete a meeting by id 
    '''
    def get_object(self, id):
        # to check if id is exist or not 
        try:
            return Zoom.objects.get(meeting_id=id)
        except Zoom.DoesNotExist:
            raise Http404

    def get(self, request, id):
        '''
        this method to get a specific meeting by id 
        '''
        data = self.get_object(id)
        serializer = MeetingSerializer(data)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        '''
        this method to update a specific meeting by id 
        then store the updated data in the database
        '''
        data = self.get_object(id)
        serializer = MeetingSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,id):
        '''
        this method to delete a specific meeting by id
        '''
        data = self.get_object(id)
        delete_meeting_from_zoom=Meeting().delete_meeting(id)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)