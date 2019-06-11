import inspect


EMPTY = inspect.Parameter.empty
POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD
VAR_POSITIONAL = inspect.Parameter.VAR_POSITIONAL
KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY
VAR_KEYWORD = inspect.Parameter.VAR_KEYWORD

def test1(a, b, *, c, d, **kwargs):
    pass

# params = inspect.signature(test1).parameters
# for name, param in params.items():
#     print(name, param.kind)