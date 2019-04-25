def encoder(func=None, encoding="utf-8"):
    def wp(func):
        def wrapper(spider, response):
            response = response.replace(body=response.body.decode(encoding))
            return func(spider, response)

        return wrapper

    if func:
        if not callable(func):
            raise Exception("ERROR! not callable")
        return wp(func)
    return wp
