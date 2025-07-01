
from log_processor import process_log

def start_worker(queue):
    while True:
        log_path = queue.get()
        try:
            process_log(log_path)
        except Exception as e:
            print(f"Error processing {log_path}: {e}")
        queue.task_done()
