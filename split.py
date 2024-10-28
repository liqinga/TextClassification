# -*- codeing = utf-8 -*-
# @Time : 2024/10/28 11:08 上午
# @Author : Li Qing
# @File : split.py
# @Software : PyCharm

import pandas as pd
import json
import random

def split_data(input_file, train_file, dev_file, test_file, train_ratio=0.7, dev_ratio=0.15):
    # 读取数据
    data = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            input_text, label = line.strip().split('\t')
            data.append({'input': input_text, 'label': label})

    # 转换为 DataFrame
    df = pd.DataFrame(data)

    # 按 label 分组
    grouped = df.groupby('label')

    train_data = []
    dev_data = []
    test_data = []

    # 按比例分配数据
    for label, group in grouped:
        group = group.sample(frac=1, random_state=42)  # 打乱组内数据
        total_size = len(group)
        train_size = int(total_size * train_ratio)
        dev_size = int(total_size * dev_ratio)

        train_data.append(group.iloc[:train_size])
        dev_data.append(group.iloc[train_size:train_size + dev_size])
        test_data.append(group.iloc[train_size + dev_size:])

    # 合并数据集
    train_data = pd.concat(train_data)
    dev_data = pd.concat(dev_data)
    test_data = pd.concat(test_data)

    # 保存数据到文件
    train_data.to_csv(train_file, sep='\t', index=False, header=False)
    dev_data.to_csv(dev_file, sep='\t', index=False, header=False)
    test_data.to_csv(test_file, sep='\t', index=False, header=False)

if __name__ == "__main__":
    split_data('/Users/liqing/PycharmProjects/OpenTextClassification/output.txt', 'train.txt', 'dev.txt', 'test.txt')
