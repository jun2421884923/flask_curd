from functools import wraps
from flask import request,current_app
import json



def jsonp_modify(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + json.dumps(
                func(*args, **kwargs)) + ')'
            return current_app.response_class(
                content, mimetype='application/javascript')
        else:
            return func(*args, **kwargs)

    return decorated_function
def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator( *args, **kwargs):
        objects = func( *args, **kwargs)
        try:
            if 'callback' in request.args.keys():
                data = json.dumps(objects)
                # a jsonp response!
                print " request.args.get('callback')=" +request.args.get('callback')
                data = '%s(%s);' % ( request.args.get('callback'), data)
                return current_app.response_class(data, mimetype='application/javascript')
            else:

                print "not callback"
                return objects
        except:
            print "except"
            data =objects
        print "try out"
        return current_app.response_class(data, mimetype='application/javascript')
    return decorator
def jsonp(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(
                func(*args, **kwargs).data) + ')'
            return current_app.response_class(
                content, mimetype='application/javascript')
        else:
            return func(*args, **kwargs)

    return decorated_function