from tasks import hello, app

def on_result(message):
    print(message)

r1 = hello.apply_async(args=('hi', 5))
r2 = hello.apply_async(args=('hello', 2))

r1.get(on_message=on_result)
r2.get(on_message=on_result)
