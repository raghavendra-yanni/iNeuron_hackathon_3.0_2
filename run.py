# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 19:19:28 2017

@author: linhb
"""

import six
import configurations
import data
import model_utils
import seq2seq_model
import sys
import numpy as np

def main(argv=None):
    if argv is None:
        mode = sys.argv[1]

    # load data from pickle and npy files
    data_path = configurations.data_path
    metadata, idx_q, idx_a = data.load_data(PATH=data_path)
    (trainX, trainY), (validX, validY), (testX, testY) = model_utils.split_dataset(idx_q, idx_a)

    # parameters 
    source_vocab_size = configurations.vocab_size + 2 # 2 extra UNK and _ (for pad)
    target_vocab_size = source_vocab_size
    source_len = configurations.source_len 
    target_len = configurations.target_len

    batch_size = configurations.batch_size
    layer_size = configurations.layer_size
    num_layers = configurations.num_layers
    model_type = configurations.model_type
    attention_heads = configurations.attention_heads
    model_path = configurations.model_path
    reverseInput = configurations.reverseInput
    learning_rate = configurations.learning_rate
    epochs = configurations.epochs

    # reverseInput
    if reverseInput == True:
        trainX = np.fliplr(trainX)
        trainY = np.fliplr(trainY)
    
    model = seq2seq_model.Seq2Seq(source_len=source_len,
                           target_len=target_len,
                           source_vocab_size=source_vocab_size,
                           target_vocab_size=target_vocab_size,
                           model_path=model_path,
                           layer_size=layer_size,
                           num_layers=num_layers,
                           model_type = model_type,
                           attention_heads = attention_heads,
                           learning_rate = learning_rate,
                           epochs = epochs
                           )
    sess = model.load_model()
                               
    if (mode.lower() == "train"):
        sess = model.train(trainX, trainY, validX, validY, batch_size)
    
    elif (mode.lower() == "test"):
        test_batch_gen = model_utils.batch_gen(testX, testY, batch_size)
        nextbatch = six.next(test_batch_gen)
        input_ = nextbatch[0]
        output_ = nextbatch[1]
        
        prediction = model.predict(sess, input_)
        
        replies = []
        for i in range(len(prediction)):
            q = data.decode(sequence=input_.T[i], lookup=metadata['idx2w'], separator=' ')
            a = data.decode(sequence=output_.T[i], lookup=metadata['idx2w'], separator=' ')
            decoded = data.decode(sequence=prediction[i], lookup=metadata['idx2w'], separator=' ').split(' ')
            if ((q.count('unk') == 0) & (a.count('unk') == 0) & (decoded.count('unk') == 0)):
                if decoded not in replies:
                    print('q : [{0}]\n a : [{1}]\n p : [{2}]\n\n'.format(q, a, ' '.join(decoded)))
                    replies.append(decoded)
               
    elif (mode.lower() == "demo"):
        print("Hey there! How can I help? Press q to when you are bored.")
        while (True):
            sys.stdout.write("QUESTION:")
            question = input()
            if (question == "q"):
                break
            
            q_indices = data.encode(sequence=question, lookup=metadata['w2idx'], separator=' ')
            idx_q = np.zeros([1, data.limit['maxq']], dtype=np.int32)
            idx_q[0] = np.array(q_indices)
            idx_q = idx_q.T
            
            idx_a = model.predict(sess, idx_q)
            answer = data.decode(sequence=idx_a[0], lookup=metadata['idx2w'], separator=' ')

            print("\nANSWER:\n" + answer)
            print("------------------")
            
        # Run demo.py for web interface chat
        # TODO: facebook messgenger app?

if __name__ == "__main__":
    main()

