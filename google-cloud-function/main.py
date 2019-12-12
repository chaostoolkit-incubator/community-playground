import datetime
import json
import sys

 INDEX_TEMPLATE = """
        <!DOCTYPE html>
        <head>
        <title>ChaosIQ cloud function</title>
        </head>
        <body>
        <h1>Hour in Range Cloud function</h1>

        <p>This is a google cloud function that can be used for safeguards with
        ChaosIQ</p>
        <p>Please add parameters giving lowerand upper bounds:</p>
        <a href="?lower=8&upper=18">hours in range link</a>
        </body>
    """


def hour_is_in_range(lower, upper):
    """returns a boolean indicating if the current hour is within bounds

    Parameters:
    lower (int): lowerbound of range
    upper (int): upper bound of range

    Returns:
    bool:True if the current our is between lower and upper, otherwise false

   """
    print(f'hourInRange with lower: {lower} and upper: {upper}')
    return datetime.datetime.now().hour in range(lower, upper)


def get_json_result(status):
    """returns a json status based on the status given

    Parameters:
    status (boolean): boolean indicating a good status or bad status

    Returns:
    json: {'status': 'ok'} for good (True), {'status': 'ko'} for bad (False)

   """
    return json.dumps({'status': 'ok'}) if status else json.dumps(
        {'status': 'ko'})


def hour_in_range(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response
          <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    print('hour_in_range called')

    print(f'request is: {request}')
    if request.args and 'lower' in request.args:
        lower = int(request.args.get('lower'))
        if 'upper' in request.args:
            upper = int(request.args.get('upper'))
            return get_json_result(hour_is_in_range(lower, upper))

    # for accessing page without arguments, shows the page with usage
    return INDEX_TEMPLATE


if __name__ == '__main__':
    res = get_json_result(hour_is_in_range(int(sys.argv[1]), int(sys.argv[2])))
    print(res)
