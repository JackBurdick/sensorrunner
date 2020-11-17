from secrets import BROKER_URL, RESULT_BACKEND, REDBEAT_URL, SERIALIZER, Q_A, Q_B, Q_C
from kombu import Queue
from kombu.serialization import registry

# use pickle
registry.enable(SERIALIZER)
task_serializer = SERIALIZER
result_serializer = SERIALIZER
accept_content = [SERIALIZER]

# dynamic
broker_url = BROKER_URL
result_backend = RESULT_BACKEND
redbeat_redis_url = REDBEAT_URL
beat_scheduler = "redbeat.RedBeatScheduler"
beat_max_loop_interval = 1
beat_schedule = {}

# queue
broker_transport_options = {"queue_order_strategy": "priority"}
task_queues = (Queue(Q_A), Queue(Q_B), Queue(Q_C))