from tasks import hello

def on_message(message):
    print(message)

r = hello.apply_async(args=('Hello World', 5))
r.get(on_message=on_message)
