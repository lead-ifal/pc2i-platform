from flask import Response
from app.models.json_encoder import JSONEncoder
#a
class GlobalController:
  def includes_all_required_params(params, body):
    includes_params = True

    for param in params:
      if (param not in body):
        includes_params = False

    return includes_params

  def generate_response(status, message, data=None):
    response = {}
    response['message'] = message

    if data is not None:
      response['data'] = data

    return Response(
      response = JSONEncoder().encode(response),
      status = status,
      mimetype = 'application/json'
    )
