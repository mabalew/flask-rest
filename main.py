import requests
from flask import Flask, request, jsonify

import os

app = Flask(__name__)

data = [{"key": 1, "service": "srv1", "value": "example 1"},
{"key": 2, "service": "srv1", "value" : "example 2"},
{"key": 3, "service": "srv1", "value" : "example 3"},
{"key": 4, "service": "srv1", "value" : "example 4"},
{"key": 5, "service": "srv1", "value" : "example 5"},
]

@app.route("/")
def index():
  header = {'message': 'This endpoint returns all the entries in dataset'}
  result = {
    'header': header,
    'entries': data
  }
  return jsonify(result)

@app.route("/<int:id>", methods=['POST', 'GET', 'PUT', 'DELETE'])
def entry(id):
  header = {'method': request.method}
 
  try:
    response = requests.request("GET", url=os.environ['MICROSERVICE2_URL'])
    print(response.json())
    header["frommicsrv2"] = str(response.json())
  except KeyError:
      return "invalid key"  
  except:
    return "error while calling micsrv2"

  """Returns one entry from data."""
  if request.method == "GET":
    try:
      for i in range(len(data)):
        if data[i]["key"] == id:
          header['message'] = 'This endpoint returns the entry {} details and response from micsrv2 service'.format(id)
          result = {"header": header,
                    "body": data[i]
          }
          return jsonify(result)
    except ValueError:
      return "invalid input"
    except KeyError:
      return "invalid key"

  elif request.method == "PUT":
    try:
      _json = request.get_json()
      for i in range(len(data)):
        if data[i]["key"] == id:
          header['message'] = 'This endpoint updates the entry {}'.format(id)
          header['json'] = _json
          data[i]["service"] = _json['service']
          data[i]["value"] = _json["value"]
          result = {"header": header,
                    "body": data[i]
          }
          return jsonify(result)
    except ValueError:
      return "invalid input"
    except KeyError:
      return "invalid key"
  elif request.method == "DELETE":
    try:
      for i in range(len(data)):
        if data[i]["key"] == id:
          header['message'] = 'This endpoint deletes the entry {} details'.format(id)
          result = {"header": header,
                    "body": data[i]
          }
          del(data[i])
          return jsonify(result)
    except ValueError:
      return "invalid input"
    except KeyError:
      return "invalid key"
  elif request.method == "POST":
    try:
      _json = request.get_json()
      header['message'] = 'This endpoint updates the entry {}'.format(id)
      header['json'] = _json
      _json["key"] = id
      data.append(_json)
      result = {"header": header,
                "body": data[len(data) - 1]}
          
      return jsonify(result)
    except ValueError:
      return "invalid input"
    except KeyError:
      return "invalid key"
    header = {"header": {'message': "Wrong method"}}

  return jsonify(header)

if __name__ == "__main__":
    app.run(host=os.environ['MICROSERVICE1_HOST']
, port=os.environ['MICROSERVICE1_PORT'], debug=True)