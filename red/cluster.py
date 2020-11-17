import celery
import celeryconf

app = celery.Celery(__name__)
app.config_from_object(celeryconf)