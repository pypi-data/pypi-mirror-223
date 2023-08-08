# aioqueueext

A package that provides asyncio Queues with additional functionality.

## Work-in-Progress

The repository contains modules extracted from my other project and was refactored as a separate package.

In the current version, I have not verified all of the functions.

Additional functions I plan to implement are:
- `return_when_*()` - async functions to ease synchronization tasks
- `set_on_get_callback()`
- `set_on_put_callback()`
- `peek_nowait()` - returns the "up-next" item without removing it from the queue
- `peek_and_get()` - async peek and conditionally get (pop) an item from the queue
