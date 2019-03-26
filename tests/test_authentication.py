import pytest
import requests

def auth_attempt():
	return requests.post("http://localhost:5000", {"username": "username", "password": "password"}.text)	

def test_authentication():
	assert "youtube" in auth_attempt()
