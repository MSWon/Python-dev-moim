from gensim.models import word2vec
from konlpy.tag import Twitter
import re


pos_tagger = Twitter()

def read_data(filename):    
    with open(filename, 'r',encoding='utf-8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]        
        data = data[1:]   # header 제외 #    
    return data 


num_features = 128  # 문자 벡터 차원 수
num_workers = 4  # 병렬 처리 스레드 수
window_size = 5  # 문자열 창 크기
vocab_size = 100000
iters = 50

train_data = read_data('./data/ratings_train.txt') 
test_data = read_data('./data/ratings_test.txt')


def tokenize(sent):
    return ['/'.join(t) for t in pos_tagger.pos(sent, norm=True, stem=True)]

def save(data, output_dir):
    with open(output_dir, 'w') as f:
        for row in data:
            _, sent, label = row
            rep_sent = " ".join(tokenize(sent))
            if(rep_sent):
                f.write(f'{rep_sent}\t{label}\n')
    print("Cleaned corpus saved")

# training Word2Vec model using skip-gram
tokens = [tokenize(row[1]) for row in train_data]
save(train_data, './data/ratings_train.cleaned.txt')
save(test_data, './data/ratings_test.cleaned.txt')
print("Now training")

model = word2vec.Word2Vec(tokens,
                          workers=num_workers,
                          size=num_features,
                          window=window_size,
                          max_vocab_size=vocab_size,
                          iter=iters,
                          sg=1)

with open('Word2vec.vocab', 'w') as f:
    for word in model.wv.index2word:
        f.write(word.strip() + "\n")

model.save('Word2vec.model')
print(model.wv.most_similar('공포/Noun', topn=20))
