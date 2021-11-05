class GlobalController:
  def includesAllRequiredParams(params, body):
    includesAllRequiredParams = True

    for param in params:
      if (param not in body):
        includesAllRequiredParams = False
    
    return includesAllRequiredParams

  def generateResponse(status, message, data=None):
    response = {}
    response['status'] = status
    response['message'] = message
    
    if data is not None:
      response['data'] = data
    
    return response