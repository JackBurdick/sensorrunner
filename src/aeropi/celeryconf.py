from secrets import BROKER_URL, RESULT_BACKEND, REDBEAT_URL, SERIALIZER
from kombu import Queue
from kombu.serialization import registry

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
task_queues = (
    Queue("collect"),
    Queue("q_demux_run"),
    Queue("q_demux_log"),
    Queue("q_dists_run"),
    Queue("q_dists_log"),
)
