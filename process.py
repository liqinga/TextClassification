# -*- codeing = utf-8 -*-
# @Time : 2024/10/28 10:51 上午
# @Author : Li Qing
# @File : process.py
# @Software : PyCharm
import json
import re


def process_jsonl_file(input_file, output_file):
    output_lines = []

    # 读取 .jsonl 文件
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)  # 解析 JSON 行
            input_text = data['input']  # 提取 input
            # 使用正则表达式提取 label 中的数字
            label_number = re.search(r'\d+', data['label']).group() if re.search(r'\d+', data['label']) else ''
            output_line = f"{input_text}\t{label_number}"  # 拼接成目标格式
            output_lines.append(output_line)

    # 输出处理后的结果
    with open(output_file, 'w', encoding='utf-8') as output_file:
        for line in output_lines:
            output_file.write(line + '\n')


if __name__ == "__main__":
    # 替换为你的文件路径
    process_jsonl_file('/data/reclor/other/test_instrument.jsonl', 'output.txt')
