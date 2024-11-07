import time
import uuid
from datetime import datetime
import math


def get_performance_timing():
    current_time = time.time() * 1000
    return {
        'requestStart': current_time - 100,
        'responseStart': current_time - 50
    }


def calculate_time_value(app_context):
    start_time = time.time() * 1000

    isr_start = app_context.get('isrStart', 0) if app_context else 0
    isr_end = app_context.get('isrEnd', 0) if app_context else 0

    ttfb = 0

    perf_timing = get_performance_timing()
    if perf_timing:
        request_start = perf_timing.get('requestStart', 0)
        response_start = perf_timing.get('responseStart', 0)

        if response_start > 0 and request_start > 0:
            ttfb = response_start - request_start

    ttfb_adjustment = ttfb - (isr_end - isr_start) if ttfb > 0 else 0
    mid_point = math.floor(isr_end + ttfb_adjustment / 2)

    current_time = datetime.now().timestamp() * 1000
    time_diff = current_time - start_time

    return math.floor((mid_point + time_diff) / 1000)


def generate_token(app_context=None):
    try:
        t = math.floor(calculate_time_value(app_context) / 30)
        n = format(t, '08X')  

        o = (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '').upper()

        result = ''
        for i in range(64):
            if i % 8 == 1:
                result += n[(i - 1) // 8]
            else:
                result += o[i]

        return result

    except Exception:
        return ''


app_context = {
    'isrStart': time.time() * 1000 - 100, # performance.now()
    'isrEnd': time.time() * 1000 # performance.now()
}
token = generate_token(app_context)
print(token)
