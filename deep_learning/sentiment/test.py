import requests

single_review = "i am happy"

url = "https://qnv9incmtj.execute-api.ap-southeast-1.amazonaws.com/Prod/predict"
data = {"body": "{\"data\": \""+single_review+"\"}"}
resp = requests.post(url, json = data)
result = resp.text
print(result)