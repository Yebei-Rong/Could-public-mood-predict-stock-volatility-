#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, Dense, Conv1D, Flatten, LSTM, GlobalMaxPooling1D, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


# In[3]:


embed_num_dims = 100
max_seq_len = 1000


# In[4]:


data = pd.read_csv('data/train.csv')


# In[6]:


sentences = data['comment_text']


# In[29]:


sentences.shape


# In[7]:


sentences[0]


# In[8]:


dictt = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']


# In[10]:


# Y: dependent variable
Y = data[dictt].values


# In[13]:


# Tokenizer
tokenizer = Tokenizer(num_words = 4000) # 规定需要保留的最大的词数
tokenizer.fit_on_texts(sentences) # 要训练的texts


# In[18]:


sequence = tokenizer.texts_to_sequences(sentences) # 返回sentences的sequence


# In[31]:


len(sequence)


# In[33]:


print(sequence[0])


# In[21]:


index_of_words = tokenizer.word_index # 讲单词映射为索引


# In[37]:


index_of_words['we']


# In[34]:


len(index_of_words)


# In[25]:


padded_seq = pad_sequences(sequence, maxlen = max_seq_len)


# In[26]:


padded_seq


# In[27]:


padded_seq.shape


# In[38]:


from keras.utils import to_categorical


# In[39]:


from sklearn.cross_validation import train_test_split


# In[40]:


X_train, X_test, Y_train, Y_test = train_test_split(padded_seq, Y, train_size = 0.55)


# In[41]:


Y_train.shape


# In[42]:


X_train.shape


# In[43]:


X_test.shape


# In[ ]:


embedd_index = {}

f = open('data/glove.6B.100d.txt')

for line in f:
    val = line.split()
    word = val[0]
    coff = np.asarray(val[1:], dtype = 'float')
    embedd_index[word] = coff
    
f.close()


# In[45]:


print('Found %s word vectors.' % len(embedd_index))


# In[46]:


embedd_index['good']


# In[56]:


embedding_matrix = np.zeros((len(index_of_words) + 1, embed_num_dims))

tokens = []
labels = []

for word, i in index_of_words.items():
    temp = embedd_index.get(word)
    
    if temp is not None:
        embedding_matrix[i] = temp
        
        # for plotting 
        tokens.append(embedding_matrix[i])
        labels.append(word)


# In[57]:


embedding_matrix.shape


# In[58]:


def tsne():
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    
    new_values = tsne_model.fit_transform(tokens[:200])
    print(new_values.shape)
    
    x = []
    y = []
    
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    plt.figure(figsize=(16,16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                    xy=(x[i], y[i]),
                    xytext=(5,2),
                    textcoords='offset points',
                    ha='right',
                    va='bottom')
        
    plt.show()
    
tsne()


# In[59]:


# embedding layer before the actual BLSTM

embedd_layer = Embedding(len(index_of_words) + 1, embed_num_dims, input_length = max_seq_len, weights = [embedding_matrix])


# In[61]:


model = Sequential()
model.add(embedd_layer)
model.add(Bidirectional(LSTM(30, return_sequences=True, dropout=0.1, recurrent_dropout=0.1)))
model.add(GlobalMaxPooling1D())
model.add(Dense(30,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(6,activation='sigmoid'))


# In[62]:


model.summary()


# In[63]:


from keras.models import model_from_json

def load():
    load_json = open('weights.json', 'r')
    loaded = load_json.read()
    
    load_json.close()
    
    load = model_from_json(loaded)
    load.load_weights('model.h5')
    print('Loaded')
    model = load


# In[64]:


from keras.optimizers import Adam

add = Adam(lr = 0.01)
model.compile(loss = 'categorical_crossentropy', optimizer=add, metrics=['accuracy'])


# In[66]:


hist = model.fit(X_train, Y_train, epochs=1, batch_size=500, validation_data=(X_test, Y_test))


# In[67]:


result = model.evaluate(X_test, Y_test)


# In[70]:


print(result)


# In[ ]:




