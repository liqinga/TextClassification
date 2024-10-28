# -*- codeing = utf-8 -*-
# @Time : 2024/10/21 12:23 上午
# @Author : Li Qing
# @File : snapshot.py
# @Software : PyCharm
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from huggingface_hub import snapshot_download
import huggingface_hub
huggingface_hub.login("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")

snapshot_download(
  repo_id="google-bert/bert-base-uncased",
  local_dir="bert-base-uncased",
  local_dir_use_symlinks=False,
  proxies = {"https": "http://localhost:7890"}
)