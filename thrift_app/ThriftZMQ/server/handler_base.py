from .ttypes import TPredictResult
import json
import numpy as np


class ModelBase():
    def __init__(self):
        print("ModelBase init")
        self.json_encoder = json.JSONEncoder()
    
    def process(self, list_input_dict):
        return 

    def serialize(self, value):
        if isinstance(value, np.ndarray): return value.tolist()  
        if isinstance(value, np.int_): return int(value)
        if isinstance(value, np.float_): return float(value)

    def convert_to_json(self, pred):
        jsonResult = {"result": self.serialize(pred)}
        return self.json_encoder.encode(jsonResult)

    def predict(self, list_input_dict):
        list_model_predict = self.process(list_input_dict)
        list_tresult = []
        for pred in list_model_predict:
            list_tresult.append(TPredictResult(errorCode=0, 
                                                jsonResult=self.convert_to_json(pred)))
        return list_tresult