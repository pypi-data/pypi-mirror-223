# event-delegate

 An event class for python.

## Usage

```python
from event_delegate import Event

my_event = Event()

my_event += print

my_event("hello, world!")
# output: hello, world!
```

## Documentation

### Handler signature:

```python
(*args, **kwargs) -> Any
```

> ![WARNING]
> A handler may return a value to be buffered.

### Event

#### The Event class takes no arguments.

```python
my_event = Event()
```

#### Adding a handler to an event. (can't add the same twice)

```python
my_event.add_handler(handler)
# or 
my_event += handler
```

#### Removing a handler from an event

```python
my_event.remove_handler(handler)
# or
my_event -= handler
```

#### Checking if a handler is added to the event

```python
my_event.has_handler(handler) # True or False
```

#### Invoking events

```python
my_event.invoke(arg1, arg2, kwarg1=1)
# or
my_event(arg1, arg2, kwarg1=1)
```

#### Checking buffered return values

```python
# after invoking my_event with [0,1,2,3]
my_event & any # true
my_event.get_return(sum) # 6
my_event & (any, all) # {<built-in function any>: True, <built-in function all>: False}
my_event.get_returns((all, sum)) # {<built-in function all>: False, <built-in function sum>: 6}
my_event.returns # {<built-in function any>: True, <built-in function all>: False, <built-in function sum>: 6}
```
