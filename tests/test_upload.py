import pytest
import requests

def auth_attempt():
	return requests.post("http://localhost:5000", {"username": "admin", "password": "password"}.text)	

def upload_attempt():
	return requests.post("http://localhost:5000/upload", {"file": "ocean.mp4"}.text)
def test_authentication():
	auth_attempt()
	assert "ocean" in auth_attempt()
