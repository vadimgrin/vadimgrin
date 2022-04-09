from functools import wraps

def mydecor(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        print(f'About to call {func.__name__} with args: {args} and kwargs: {kwargs}')
        func(*args, **kwargs)
        print('End')
    return wrapper_func

@mydecor
def runsample(header: str ='My Header', line: str = None) -> int:
    print(header)
    print(f'The line is {line}')


if __name__ == '__main__':
    runsample('This is my header', line = 'Hello World')
