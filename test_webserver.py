import pytest
import requests

def hello_world():
	return requests.get("http://localhost").text	

def test_hello_world():
	assert "Hello World" in hello_world()
