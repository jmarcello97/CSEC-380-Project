import pytest
import requests
import time

def auth_attempt():
	correct_login = requests.post("http://localhost:5000", {"username": "admin", "password": "password"}).text
	incorrect_username = requests.post("http://localhost:5000", {"username": "asd", "password": "password"}).text
	incorrect_password = requests.post("http://localhost:5000", {"username": "admin", "password": "asd"}).text

	return "Invalid username" in incorrect_username and "Invalid password" in incorrect_password and "Upload from Link" in correct_login
 
def upload_attempt():
	s = requests.session()
	auth = s.post("http://localhost:5000", {"username": "admin", "password": "password"})
	upload = s.post("http://localhost:5000/upload", files={"file": open('ocean.mp4', 'rb')}).text
	upload_success = "ocean.mp4" in upload
	get_video = s.get("http://localhost:5000/static/videos/ocean.mp4").status_code
	get_video_success = get_video == 200
	delete = s.get("http://localhost:5000/delete_video/ocean.mp4").text
	delete_success = "ocean.mp4" not in delete
	return upload_success and delete_success and get_video_success

def test_authentication():
	assert auth_attempt()
	assert upload_attempt()
