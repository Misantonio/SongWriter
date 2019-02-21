import utils
import random
import numpy as np
from songwriter import Songwriter

def write_each_char():
    corpus = utils.read_corpus()#replace('\r', ' ')#.replace('\n', ' ')

    vocab = list(set(corpus))
    char_ix = {c:i for i,c in enumerate(vocab)}
    ix_char = {i:c for i,c in enumerate(vocab)}

    maxlen = 100
    epochs = 50
    vocab_size = len(vocab)

    sentences = []
    next_val = []
    for i in range(len(corpus)-maxlen-1):
        sentences.append(corpus[i:i+maxlen])
        next_val.append(corpus[i+maxlen])

    X = np.zeros((len(sentences), maxlen, vocab_size))
    Y = np.zeros((len(sentences), vocab_size))
    for ix in range(len(sentences)):
        Y[ix, char_ix[next_val[ix]]] = 1
        for iy in range(maxlen): 
            X[ix, iy, char_ix[sentences[ix][iy]]] = 1

    model = Songwriter()
    model.add_final_layer(100, (maxlen, vocab_size))

    history = model.train((X, Y), epochs, True, True)

    generated = ''
    start_index = random.randint(0, len(corpus)-maxlen-1)
    sent = corpus[start_index:start_index+maxlen]
    generated+=sent
    for i in range(200):
        x_sample = generated[i:i+maxlen]
        x = np.zeros((1, maxlen, vocab_size))
        for j in range(maxlen):
            x[0, j, char_ix[x_sample[j]]] = 1
        probs = model.predict(x)
        ix = np.random.choice(range(vocab_size), p=probs.ravel())
        generated += ix_char[ix]

    print('"{}\n\n"'.format(generated))

if __name__ == "__main__":
    write_each_char()
    