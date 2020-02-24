import json
import os
from typing import Dict

class DataPack:
    """

    """
    def __init__(self, data_dict:Dict):
        """
        get the basic terms includes:
        title[str]    context[str]    question[str]    id[str]    answers[list]    is_impossible

        :param data_dict: the datadict from SQuAD dataset
        """
        data_list = data_dict.get("data")
        self.data_pair = []
        for data in data_list:
            # get the title term
            title = data.get("title")
            # get the context term
            paras = data.get("paragraphs")
            for para in paras:
                context = para.get("context")
                qas = para.get("qas")
                for qa in qas:
                    temp = None
                    try:
                        ques, idx, ans, is_impossible = qa.values()
                    except ValueError as e:
                        ans, ques, idx, _, is_impossible = qa.values()
                        temp = [title, context, ques, idx, ans, is_impossible]
                    else:
                        temp = [title, context, ques, idx, ans, is_impossible]
                    self.data_pair.append(temp)

class SQuAD_Dataset:
    """

    """
    default_path = os.path.abspath("E:\DATASET\SQuad")
    train_name = "train-v2.0.json"
    dev_name = "dev-v2.0.json"
    predict_name = "prediction-v2.0.json"

    def __init__(self, basepath=None):
        """

        :param filename: the base_path
        """
        if basepath is None:
            basepath = SQuAD_Dataset.default_path
        train_file = os.path.join(basepath, SQuAD_Dataset.train_name)
        dev_file = os.path.join(basepath, SQuAD_Dataset.dev_name)
        # pred_file = os.path.join(basepath, SQuAD_Dataset.predict_name)

        # file_tuple = (train_file, dev_file, pred_file)
        file_tuple = (train_file, dev_file)
        # read the data
        raw_data_list = []
        for file in file_tuple:
            with open(file, 'r') as f:
                raw_data_list.append(json.load(f))

        # parse the data
        data_list = [self.parse_raw_data(data) for data in raw_data_list]

        self.train, self.dev = data_list


    def parse_raw_data(self, raw_data:Dict) -> DataPack:
        return DataPack(raw_data)

if __name__ == '__main__':
    dataset = SQuAD_Dataset()
    train = dataset.train.data_pair
    i = 0
    for item in train:
        if len(item[4]) > 1:
            i += 1
