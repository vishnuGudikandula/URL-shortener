from flask import Flask, request, render_template
import threading
from queue import Queue
from worker import start_worker
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'test_logs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

task_queue = Queue()

# Start background workers
for _ in range(4):
    threading.Thread(target=start_worker, args=(task_queue,), daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def upload_log():
    if request.method == "POST":
        file = request.files["logfile"]
        filepath = os.path.abspath(os.path.join(UPLOAD_FOLDER, file.filename))
        file.save(filepath)
        task_queue.put(filepath)
        return "Log uploaded and sent for processing!"
    return render_template("upload.html")

@app.route("/metrics")
def metrics():
    from models import get_latest_metrics
    data = get_latest_metrics()
    return {"metrics": data}

if __name__ == "__main__":
    app.run(debug=True)
