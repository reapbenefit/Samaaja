import json
from werkzeug.wrappers import Response

def custom_response(message=None, data={}, status_code=200, error=False):
    """
    Generate a custom HTTP response in JSON format.

    Parameters:
        message (str, optional): A message to include in the response. Defaults to None.
        data (dict, optional): The data to include in the response. Defaults to an empty dictionary.
        status_code (int, optional): The HTTP status code for the response. Defaults to 200.
        error (bool, optional): A flag to indicate if the response is an error. Defaults to False.

    Returns:
        Response: A Werkzeug `Response` object containing the JSON response.
    """
    # Create a new Response object
    response = Response()

    # Set the response mimetype and charset
    response.mimetype = 'application/json'
    response.charset = 'utf-8'

    # Set the status code for the response
    response.status_code = status_code

    # Determine the status of the response (success or error)
    status = "error" if error else "success"

    # Prepare the response data in JSON format
    response.data = json.dumps(
        {"message": message, "status": status, "data": data}, default=str
    )

    # Return the response object
    return response