from flask import Response
from app.models.json_encoder import JSONEncoder

class GlobalController:
  def includesAllRequiredParams(params, body):
    includesAllRequiredParams = True

    for param in params:
      if (param not in body):
        includesAllRequiredParams = False
    
    return includesAllRequiredParams

  def generateResponse(status, message, data=None):
    response = {}
    response['message'] = message
    
    if data is not None:
      response['data'] = data
    
    return Response(
      response = JSONEncoder().encode(response),
      status = status,
      mimetype = 'application/json'
    )
