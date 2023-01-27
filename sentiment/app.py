import json
import pickle



def lambda_handler(event, context):

    body = json.loads(json.loads(event["body"])["body"])
    payload = body["data"]
    
    with open('./ml_model.p', 'rb') as pickled:
        data = pickle.load(pickled)
    model = data['model']
    vectorizer = data['vectorizer']

    vector = vectorizer.transform([payload])
    prediction = model.predict(vector)[0]
    response = prediction

    return {
        "statusCode": 200,
        "body": json.dumps(
            response
        ),
    }
