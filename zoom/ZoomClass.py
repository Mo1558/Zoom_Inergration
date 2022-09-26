import jwt
import json
import requests
from time import time
from decouple import config
from rest_framework.response import Response

class Token:
	'''
	class for generateToken by API_KEY and API_SECRET
	'''
	def __init__(self):
		self.API_KEY = config('API_KEY')
		self.API_SECRET = config('API_SECRET')
	

	def createToken(self):
		'''
		method to create a new token from zoom by jwt token
		'''
		token = jwt.encode({'iss': self.API_KEY, 'exp': time() + 5000},self.API_SECRET,algorithm='HS256')
		return token




class Actions(Token):
	'''
	class for make actions like create meetings , get meetings , delete meetings
	and get all meetings
	'''

	def __init__(self):
		self.headers = {'authorization': f'Bearer {self.createToken()}',
		'content-type': 'application/json'}


	def create(self,create_url,data,):
		'''
		method to create a new meeting by using create_url , headers 
		and data 
		'''
		post_request=requests.post(f'{create_url}',headers=self.headers, data=data)
		return post_request
	
	
	def delete(self,delete_url):
		'''
		method to delete a metting by using delete_url and headers
		'''
		delete_data=requests.delete(f'{delete_url}',headers=self.headers)
		return delete_data



class Meeting(Actions):
	'''
	It is the main class for take action (create , get or delete) 
	and check  if it is valid or not.  
	'''

	def __init__(self):
		self.base_url=config('base_url')
		self.headers = {'authorization': f'Bearer {Token().createToken()}',
		'content-type': 'application/json'}


	def create_meeting(self):
		'''
		this method to create a new meetingby using create method
		from action class.then check if response is valid or not. 
		if not, it will handle the error
		'''
		create_url=self.base_url+'/users/me/meetings'

		meetingdetails ={
				"topic": "test",
				"type": 2,
				"start_time": "2022-10-14T10: 21: 57",
				"duration": "45",
				"timezone": "Africa/Cairo",
				"agenda": "test",
				"recurrence": 
				{"type": 1,"repeat_interval": 1},
				"settings":	   
				{"host_video": "true",
				"participant_video": "true",
				"join_before_host": "False",
				"mute_upon_entry": "False",
				"watermark": "true",
				"audio": "voip",
				"auto_recording": "cloud"
				}
				}

		data=json.dumps(meetingdetails)						#to convert the dict to a json object
		
		try:
			request_data =self.create(create_url=create_url, data=data)
		except :
			return Response('Connection error')

		if request_data.status_code == 201:					#check if the response is successfully
			return request_data.json()
			
		elif request_data.status_code ==401:				#check if thr token is valid
			return request_data.json()['message']


		else:
			return "Meeting did not create "
	

	def delete_meeting(self,id):
		'''
		this method for deleting a specific meeting by using
		delete method from action class. and handeling the error 
		'''
		self.id=id
		delete_url=self.base_url+f'/meetings/{self.id}'
		detele_data =self.delete(delete_url=delete_url)

		if detele_data.status_code == 204: 	                 #check if response was successful
			return 'Deleted'

		elif detele_data.status_code == 401:			     #check if token is invalid				
			return detele_data.json()['message']

		elif detele_data.status_code ==404:					 #check if id is invalid		
			return detele_data.json()['message']

		else:
			return 'Can not delete meeting'


print(Meeting().create_meeting())

