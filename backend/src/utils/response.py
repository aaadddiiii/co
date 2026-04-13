def success(data=None, message=""):
    return {
        "success": True,
        "message": message,
        "data": data
    }, 200


def error(message, code=400):
    return {
        "success": False,
        "error": message
    }, code