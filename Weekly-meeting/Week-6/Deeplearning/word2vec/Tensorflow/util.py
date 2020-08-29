import numpy as np
import re
from stopwords import stopwords

BUFFER_SIZE = 2000

class Generator(object):

    def __init__(self, corpus_path, vocab_size, batch_size, window_size, shuffle=True):
        self.corpus_path = corpus_path
        self.vocab_size = vocab_size
        self.batch_size = batch_size
        self.window_size = window_size
        self.shuffle = shuffle

        self._get_vocab()
        self.gen = self._generator()


    def _get_vocab(self):
        print("Now building vocab")
        print(f"corpus : {self.corpus_path} vocab_size : {self.vocab_size}")
        f = open(self.corpus_path)

        ## Count words
        word_cnt_dict = {}
        for sent in f:
            rep_sent = re.sub("[^\w\s']", "", sent.strip())
            uncased_sent = rep_sent.strip().lower()
            for word in uncased_sent.split():
                if word not in stopwords:
                    if word not in word_cnt_dict:
                        word_cnt_dict[word] = 1
                    else:
                        word_cnt_dict[word] += 1

        ## Sort words by freq
        sorted_cnt_dict = sorted(word_cnt_dict.items(), key=lambda x: x[1], reverse=True)

        ## for <unk>, <pad>
        self.word2idx = {"<pad>": 0, "<unk>": 1}
        self.idx2word = {0: "<pad>", 1: "<unk>"}

        ## build vocab
        with open(f"{self.corpus_path}.vocab", "w") as f_vocab:
            total_cnt = 0
            for word, _ in sorted_cnt_dict:
                if total_cnt == self.vocab_size - 2:
                    break
                self.word2idx[word] = len(self.word2idx)
                self.idx2word[len(self.idx2word)] = word
                f_vocab.write(word + "\n")
                total_cnt += 1


    def _convert_word2idx(self, word):
        if word not in self.word2idx:
            word = "<unk>"
        return self.word2idx[word]


    def _generator(self):
        f = open(self.corpus_path)
        for sent in f:
            rep_sent = re.sub("[^\w\s']", "", sent.strip())
            uncased_sent = rep_sent.strip().lower()
            words = uncased_sent.split()
            words = [word for word in words if word not in stopwords]

            ids = list(map(self._convert_word2idx, words))
            length = len(words)
            for i in range(0, length):
                # 왼쪽 window size 만큼
                for j in range(max(0, i - self.window_size), i):
                    yield [ids[i], ids[j]]
                # 오른쪽 window size 만큼
                for j in range(i + 1, min(length, i + self.window_size + 1)):
                    yield [ids[i], ids[j]]


    def next(self):
        result_x = []
        result_y = []
        for i in range(self.batch_size):
            try:
                x, y = next(self.gen)
                result_x.append(x)
                result_y.append(y)
            except:
                self.gen = self._generator()
        if self.shuffle:
            shuffle_mask = np.random.permutation(len(result_x))
            result_x = np.array(result_x)[shuffle_mask]
            result_y = np.array(result_y)[shuffle_mask]
        return result_x[:self.batch_size], result_y[:self.batch_size]