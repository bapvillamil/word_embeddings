import json
import pickle


def rev_one_hot(x):
    l = []
    m = [l]
    for i in x:
        for j in i:
            if j < 0.5:
                j = 0
                l.append(j)
            else:
                j = 1
                l.append(j)
    return m

def to_categ(pred):

    if pred == [[1, 0, 0]]:
        return "negative"
    
    elif pred == [[0, 0, 1]]:
        return "positive"

    else:
        return "neutral"


def lambda_handler(event, context):

    body = json.loads(json.loads(event["body"])["body"])
    payload = body["data"]
    
    with open('./dl_model.p', 'rb') as pickled:
        dl_model = pickle.load(pickled)
    model = dl_model['model']
    vectorizer = dl_model['vectorizer']
    svd = dl_model["svd"]

    vector = vectorizer.transform([payload])
    sv = svd.transform(vector)
    prediction = model.predict(sv)
    prediction = rev_one_hot(prediction)
    prediction = to_categ(prediction)

    response = prediction

    return {
        "statusCode": 200,
        "body": json.dumps(
            response
        ),
    }
