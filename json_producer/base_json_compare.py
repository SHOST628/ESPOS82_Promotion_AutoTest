from frozen_path import cur_path
import json as js
import os


project_path = cur_path()
model_base_json_path = os.path.join(project_path, 'json_model\\base\\base.json')


# TODO 对比两个json串所有层级
def compare_json_key(test_cls, data_base_json, model_base_json_path):
    data_json_keys = []
    model_json_keys = []
    data_base_json = js.loads(data_base_json)
    for key in data_base_json.keys():
        data_json_keys.append(key)
    with open(model_base_json_path, 'r', encoding='utf-8') as f:
        model_json = js.load(f)
        for key in model_json.keys():
            model_json_keys.append(key)
    if data_json_keys != model_json_keys:
        test_cls.skipTest('请检查config.ini [JsonModel] 下的BaseJson 是否正确配置')
    return data_base_json


