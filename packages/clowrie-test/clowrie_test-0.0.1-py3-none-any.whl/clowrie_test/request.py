# import requests module
import requests

# Making a get request
response = requests.get('http://127.0.0.1:32326/pypi/default-test/pypi-local2/simple')

# print response
print(response.reason)

# print the reason
print(response.raw)