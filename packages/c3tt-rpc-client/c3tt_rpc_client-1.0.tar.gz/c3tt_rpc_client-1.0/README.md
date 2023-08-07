# Python Client Library for C3-Ticket-Tracker

Client-Library for [C3-Ticket-Tracker](https://github.com/crs-tools/tracker).

## Example

Get the next Encoding-Ticket, work on it and set it Done:

```python
import os
import socket

from src.c3tt_rpc_client import C3TTClient

cli = C3TTClient(os.environ['CRS_TRACKER'], os.environ['CRS_TOKEN'], socket.gethostname(), os.environ['CRS_SECRET'])
ticket = cli.assign_next_unassigned_for_state(ticket_type='encoding', to_state='encoding')
if ticket is None:
    print('No Ticket for encoding')
else:
    print('Got Ticket for encoding:')
    print(ticket)

    print('Set Ticket done')
    cli.set_ticket_done(ticket)
```

## Deploying

To Deploy a new Version to pypi, run `./upload_dist.sh`. This will

- Clean previous Build-Results
- Setup a venv
- Install build/dist Tooling (built, twine, flake8)
- Lint the Code
- Create whl and tar.gz artifacts
- Upload them to pypi
