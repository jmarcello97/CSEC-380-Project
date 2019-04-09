import pytest
import requests

def upload_attempt():
	s = requests.session()
	auth = s.post("http://localhost:5000", {"username": "admin", "password": "password"})
	upload = s.post("http://localhost:5000/upload", files={"file": open('ocean.mp4', 'rb')}).text
	upload_success = "ocean.mp4" in upload
	delete = s.get("http://localhost:5000/delete_video/ocean.mp4").text
	delete_success = "ocean.mp4" not in delete
	return upload_success and delete_success

def test_authentication():
	assert "ocean.mp4" in upload_attempt()
