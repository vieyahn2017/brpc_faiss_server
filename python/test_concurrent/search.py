from locust import HttpLocust, TaskSet, task
import numpy as np
import base64
import json
import os
from collections import deque
from data import *

ACC = 0


class WebsiteTasks(TaskSet):

    chunk_id = int(os.environ["CHUNK_IDX"])
    n_split = int(os.environ["N_SPLIT"])
    db_name = os.environ["NAME"]
    file_path = os.environ["FILE_PATH"]

    ann_dataset = BigannData1M(file_path, n_split)
    dim = ann_dataset.dim
    cids, fids, features = ann_dataset.get_query()
    gt_ids = ann_dataset.get_groundtruth()

    cids = deque(cids)
    fids = deque(fids)
    features = deque(features)
    gt_ids = deque(gt_ids)

    def on_start(self):
        pass

    @task
    def search(self):
        request_data = {
            "db_name": self.db_name,
            "b64_feature": self.features.popleft(),
            "topk": 20,
        }
        request_data = json.dumps(request_data)
        response = self.client.post("search", data=request_data)
        result = json.loads(response.text)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks  # 指向TasSet类，定义测试行为
    min_wait = 0
    max_wait = 0
