import traceback

def handle_error(exception):
    print(f'Error: {exception}')
    traceback.print_exc()