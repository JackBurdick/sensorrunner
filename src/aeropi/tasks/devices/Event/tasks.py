import importlib

import aeropi

importlib.reload(aeropi)

from aeropi.celery_app import setup_app
from aeropi.sa import SESSION_VIB801S, VIB801S_Row


app = setup_app()


@app.task(bind=True, queue="q_log_event_entry")
def _log_event_entry(self, entry):
    if entry:
        if isinstance(entry, VIB801S_Row):
            entry.add(SESSION_VIB801S)
        else:
            raise ValueError(f"unable to match entry {entry} to accepted row types")
    else:
        pass

    return entry


# @app.task(ignore_result=True)
@app.task(bind=True, queue="collect")
def event_entry(self, entry):
    return _log_event_entry.s(entry).apply_async()
