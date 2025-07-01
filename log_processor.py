
from models import insert_metrics
import re
from collections import Counter
from datetime import datetime

def process_log(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    error_count = 0
    ip_counter = Counter()
    time_buckets = Counter()

    for line in lines:
        if "ERROR" in line:
            error_count += 1
        match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
        if match:
            ip_counter[match.group()] += 1
        time_match = re.search(r'\d{2}:\d{2}:\d{2}', line)
        if time_match:
            hour = time_match.group().split(":")[0]
            time_buckets[hour] += 1

    metrics = {
        "filename": filepath,
        "errors": error_count,
        "ip_hits": dict(ip_counter),
        "hourly_traffic": dict(time_buckets),
        "processed_at": datetime.utcnow()
    }

    insert_metrics(metrics)
