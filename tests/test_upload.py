import pytest
import requests

def upload_attempt():
	s = requests.session()
	auth = s.post("http://localhost:5000", {"username": "admin", "password": "password"})
	upload = s.post("http://localhost:5000/upload", files={"file": open('ocean.mp4', 'rb')}).text
	print(upload)
	return upload


def test_authentication():
	assert "ocean.mp4" in upload_attempt()
