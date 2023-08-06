import os
from typing import Any, Union
from ._iort_engine_ import IORTEngine
import pandas as pd
from datetime import datetime
from pytz import timezone
from tqdm import tqdm
import time

class EngineEvaluator:
    def __init__(self, engine:IORTEngine, dataset:Any) -> None:
        try:
            _ = iter(dataset)
        except TypeError as te:
            print(dataset, 'is not iterable')
        self.engine = engine
        self.dataset = dataset
        self.process_log = self.create_process_log()

    def create_process_log(self):
        # init
        dataset = self.dataset

        return {
            "start_time":"None",
            "iter_logs":[],
            "number_of_epoch" : len(dataset),
        }

    def save_testdata(self, result_csv_path:str, additional_info:Union[dict, None] = None):
        #init
        path:str = result_csv_path
        process_log:dict = self.process_log
        infos = {}
        
        infos.update(process_log)
        if additional_info:
            infos.update(additional_info)
        keys = [k for k in infos]
        keys.remove("iter_logs")
        iter_logs = pd.DataFrame(infos["iter_logs"]).to_csv()
        with open(path, 'w') as f:
            for key in keys:
                f.write(f"{key} : {infos[key]}\n")
            for s in iter_logs:
                f.write(s)

    def run(self):
        # init
        dataset = self.dataset
        engine = self.engine
        self.process_log = self.create_process_log()
        process_log = self.process_log
        process_log["start_time"] = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d-%H-%M-%S")

        # run
        process_start = time.time()
        for idx in tqdm(range(len(dataset))):
            log = {}
            _key_ = "load_data"
            log[_key_] = time.time()
            loaded_data = dataset[idx]
            log[_key_] = time.time() - log[_key_]

            _key_ = "set_input_data"
            log[_key_] = time.time()
            engine.set_input_data(data=loaded_data)
            log[_key_] = time.time() - log[_key_]

            _key_ = "convert_data2input"
            log[_key_] = time.time()
            engine.convert_data2input()
            log[_key_] = time.time() - log[_key_]

            _key_ = "move_host2device"
            log[_key_] = time.time()
            engine.move_host2device()
            log[_key_] = time.time() - log[_key_]

            _key_ = "inference"
            log[_key_] = time.time()
            engine.inference()
            log[_key_] = time.time() - log[_key_]

            _key_ = "move_device2host"
            log[_key_] = time.time()
            engine.move_device2host()
            log[_key_] = time.time() - log[_key_]

            _key_ = "convert_output2data"
            log[_key_] = time.time()
            engine.convert_output2data()
            log[_key_] = time.time() - log[_key_]

            _key_ = "get_output_data"
            log[_key_] = time.time()
            result_images = engine.get_output_data()
            log[_key_] = time.time() - log[_key_]

            _key_ = "save_data"
            log[_key_] = time.time()
            # TODO!!
            # os.makedirs(result_image_path, exist_ok=True)
            # cv2.imwrite(result_image_path.format(name=f"{idx:08d}.bmp"), result_images[0])
            log[_key_] = time.time() - log[_key_]
            process_log["iter_logs"].append(log)
        process_end = time.time()
        process_log["processing_time"] = process_end - process_start
        process_log["end_time"] = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d-%H-%M-%S")