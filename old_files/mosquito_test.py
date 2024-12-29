#!/usr/bin/env python3
# Standard library modules.

# Third party modules.

# Local modules
import mosquito
from mosquito.tests import httpbin

# Globals and constants variables.


# Register attribute callback using a decorator ...
@mosquito.attribute('headers')
def headers():
    for name in ('linux', 'mac', 'windows'):
        yield {'user-agent': name}


# ... or register attributes by hand.
mosquito.register_attributes(delay=.0, params=[{'foo': 42}, {'bar': 13, 'baz': 37}])


# Let's list all available attributes.
print('available:', mosquito.available_attributes())


with mosquito.swarm(repeat_on=(503,), max_attempts=3) as scheduler:
    # Note that the swarm uses 2 sessions only, determined by the minimum length of passed
    # attributes which is `params` in our case.
    print(f'swarm uses {len(scheduler.swarm)} sessions')

    for i in range(5):
        # `swarm wraps` requests' api and therefore supports get, post, put etc.
        # parameters passed directly to request method will overwrite such registered before
        result = scheduler.get(httpbin('/user-agent'), params=dict(bar=0))
        print(i, result.url, result.json())

    # Let's provoke an error ...
    try:
        scheduler.get(httpbin('/status/404'))

    except mosquito.MosquitoError as mre:
        print(mre)

    # ... and another one, being more obstinate this time
    try:
        scheduler.get(httpbin('/status/503'))

    except mosquito.MosquitoError as mre:
        print(mre)