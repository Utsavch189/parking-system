import uuid
import time

def generate_unique_id():
    unique_id = uuid.uuid4()
    current_time_millis = int(time.time() * 1000)
    combined_id = str(current_time_millis) + str(unique_id).replace('-', '')
    return combined_id