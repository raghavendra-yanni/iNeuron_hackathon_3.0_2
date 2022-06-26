# -*- coding: utf-8 -*-

data_path = 'datasets/twitter/'
model_path = 'models/twitter/'
#data_path = 'datasets/cornell-movie/'
#model_path = 'models/cornell-movie/'
vocab_size = 8000
source_len = 20
target_len = 20
layer_size = 512 #512
num_layers = 3  # 3
model_type = 1 #1 - Seq2Seq; 2 - Seq2Seq with attention # 3 - tied Seq2Seq
attention_heads = 1
reverseInput = False
batch_size = 64
learning_rate=0.001
epochs=30
