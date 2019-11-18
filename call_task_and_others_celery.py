from celery import group, chain, chord, signature
from proj.tasks import add, mul, xsum, hello


print(group(add.s(i, i) for i in range(10))().get())
g = group(add.s(i) for i in range(200))
print(g(10).get())

# (4 + 4) * 9
print(chain(add.s(4, 4) | mul.s(9))().get())

# (? + 4) * 8
c = chain(add.s(4) | mul.s(8))
print(c(4).get())


print(chord((add.s(i, i) for i in range(10)), xsum.s())().get())


a = add.apply_async(args=(1, 1), kwargs={}, countdown=10, expires=120)
r = add.s(1, 1).apply_async(countdown=10)
print(r.state)


def on_raw_message(body):
    print(body)


r = hello.apply_async(args=(3, 5))
print(r.get(on_message=on_raw_message, propagate=False))


r = signature('tasks.add', args=(2, 2), countdown=10)
print(r)
r = add.signature((2, 2), {}, countdown=10)
print(r.args, r.kwargs, r.options)