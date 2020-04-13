# Celery contrib

[Celery](http://www.celeryproject.org/) is a well known distributed task
queue for Python. The task is the main abstraction you work with in
Celery.

!!! note

    All your task definitions should contain a single line passing all
    the work to some attribute of the `Injector` subclass.  The only
    work you're allewed to do inside the task - prepare arguments for
    the service layer and convert result of the service layer.

## Define a task

```pycon

>>> from celery import Celery
>>> from dependencies import Injector

>>> class Say:
...
...     def __init__(self, name):
...         self.name = name
...
...     def __call__(self):
...         return 'Hello %s.' % self.name

>>> class SayHello(Injector):
...     say = Say


>>> celery = Celery('app')
>>> celery.conf.update({'task_always_eager': True})

>>> @celery.task
... def say_hello_task(*args):
...     return SayHello.let(name=args[0]).say()

>>> say_hello_task.delay('world').get()
'Hello world.'

```

As you can see, the only work we do in the tasks is arguments
preparation. It does not make much difference if we put arguments in
the injection scope or pass them directly to the callable.

!!! note

    Service objects such `Say` should not even know if they are
    executed inside the task or not.

## Define a shared task

```pycon

>>> from celery import shared_task
>>> from celery.exceptions import Reject

>>> class Process:
...
...     def __call__(self, order_id):
...         pass

>>> class ProcessOrder(Injector):
...     process = Process

>>> @shared_task
... def process_order_task(**kwargs):
...     result = ProcessOrder.process(kwargs['order_id'])
...     if not result:
...         raise Reject()

>>> process_order_task.delay()  # doctest: +ELLIPSIS
<EagerResult: ...>

```

As in the previous example, we only prepare the right arguments to the
servise layer. We also have the abbility to interpret the result of
the service layer from the perspective of the taks execution. We
don't interpret the result of the service layer in the task to bake
business decissions based on it.

## Retry tasks

[Celery](http://www.celeryproject.org/) offers you bound tasks for the
purpose of retrying the same task few times. If you decided to use
dependency injection, you don't want your business objects to know
about implementation details such as task queues, wsgi frameworks,
etc.

We can use the bound task in a clean way without abusing your business
logic with implementation details.

```pycon

>>> class Process:
...
...     def __init__(self, retry):
...         self.retry = retry
...
...     def __call__(self):
...         self.retry()

>>> class ProcessOrder(Injector):
...     process = Process

>>> @shared_task(bind=True)
... def process_order_task(self, **kwargs):
...     return ProcessOrder.let(retry=self.retry).process()

```

You should not think about `retry` in the `Process` object as retry of
the task. But retry of the business process. It's ok to have
different signatures of this two retries.

## Using Canvas

Usually, you schedule tasks somewhere in your own code. Calling
`task.delay()` method is the most common way to do that. To decouple
the class which should schedule the task, and the class implementing
the task it's a common approach to use [Celery
canvas](https://docs.celeryproject.org/en/stable/userguide/canvas.html).

You could inject signature objects to the service layer to schedule
execution of the other parts of the service layer in a task.

It is also possible to decouple business logic which should delay a task
from knowing this is a task.

```pycon

>>> from celery import signature

>>> class Submit:
...
...     def __init__(self, schedule_processing):
...         self.schedule_processing = schedule_processing
...
...     def __call__(self, order_form):
...         if order_form['was_paid']:
...             self.schedule_processing(order_form['id'])

>>> class SubmitOrder(Injector):
...     submit = Submit
...     schedule_processing = signature('app.tasks.process_order_task').delay

>>> SubmitOrder.submit({'id': 1, 'was_paid': False})

```

In this case, your business logic can use `schedule_processing` as a
regular function without knowing anything about task queues.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
