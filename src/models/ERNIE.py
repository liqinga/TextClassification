# coding: UTF-8
import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer, AutoModelForMaskedLM, AutoTokenizer
from tools.modeling_ernie import ErnieModel


class Config(object):
    """配置参数"""

    def __init__(self, dataset, pretrained_name_or_path=None):
        self.model_name = 'ERNIE'
        self.train_path = dataset + '/data/train.txt'  # 训练集
        self.dev_path = dataset + '/data/dev.txt'  # 验证集
        self.test_path = dataset + '/data/test.txt'  # 测试集
        self.class_list = [x.strip() for x in open(
            dataset + '/data/class.txt').readlines()]  # 类别名单
        self.save_path = dataset + '/saved_dict/' + self.model_name + '.ckpt'  # 模型训练结果
        self.log_path = dataset + '/log/' + self.model_name
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 设备

        self.require_improvement = 1000  # 若超过1000batch效果还没提升，则提前结束训练
        self.multi_label = False
        self.num_classes = len(self.class_list)  # 类别数
        self.num_epochs = 10  # epoch数
        self.batch_size = 128  # mini-batch大小
        self.pad_size = 32  # 每句话处理成的长度(短填长切)
        self.learning_rate = 5e-5  # 学习率
        self.bert_path = './ERNIE_pretrain' if not pretrained_name_or_path else pretrained_name_or_path
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        # self.tokenizer = AutoTokenizer.from_pretrained(self.bert_path)  # transformers4.22开始支持ernie
        print(self.tokenizer)
        self.hidden_size = 768


class Model(nn.Module):

    def __init__(self, config):
        super(Model, self).__init__()
        # self.bert = BertModel.from_pretrained(config.bert_path)
        self.bert = ErnieModel.from_pretrained(config.bert_path)
        # self.bert = AutoModelForMaskedLM.from_pretrained(config.bert_path)# transformers4.22开始支持ernie
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc = nn.Linear(config.hidden_size, config.num_classes)

    def forward(self, x):
        context = x[0]  # 输入的句子
        mask = x[2]  # 对padding部分进行mask，和句子一个size，padding部分用0表示，如：[1, 1, 1, 1, 0, 0]
        _, pooled = self.bert(context, attention_mask=mask, return_dict=False)
        out = self.fc(pooled)
        return out
