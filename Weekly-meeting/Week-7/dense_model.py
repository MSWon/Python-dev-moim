import tensorflow as tf
import numpy as np
from gensim.models import Word2Vec


class Model(object):

    def __init__(self, vocab_path, max_len, learning_rate):
        self.vocab_path = vocab_path
        self.max_len = max_len
        self.learning_rate = learning_rate

    def build_embed(self):
        model = Word2Vec.load(self.vocab_path)
        dim = model.wv[model.wv.index2word[0]].shape[0]
        embedding_matrix = np.zeros((len(model.wv.vocab), dim))
        for i in range(len(model.wv.vocab)):
            embedding_vector = model.wv[model.wv.index2word[i]]
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        return embedding_matrix

    def build_model(self, features):
        # Convert to wordemb via Lookup table
        embedding_matrix = self.build_embed()
        saved_embeddings = tf.constant(embedding_matrix, dtype=tf.float32)
        embedding_weights = tf.Variable(initial_value=saved_embeddings, trainable=False)
        word_emb = tf.nn.embedding_lookup(embedding_weights, features['input'])  # (N, max_len, dim)

        # Average Pooling
        masks = tf.sequence_mask(lengths=features['seq_len'], maxlen=self.max_len, dtype=tf.float32)  # (N, max_len)
        masks = masks[:,:, None]  # (N, max_len, 1)
        word_emb *= masks  # (N, max_len, dim)
        sum_word_emb = tf.reduce_sum(word_emb, axis=1)  # (N, dim)
        avg_emb = sum_word_emb / tf.cast(tf.expand_dims(features['seq_len'], axis=1), dtype=tf.float32) # (N, dim)

        # Build Model Graph
        L1 = tf.layers.dense(avg_emb, avg_emb.shape[1]*2)  # (N, 2*dim)
        L2 = tf.layers.dense(L1, avg_emb.shape[1])  # (N, dim)
        logits = tf.layers.dense(L2, 2)  # (N, 2)
        return logits

    def build_loss_acc(self, features):
        logits = self.build_model(features)  # (N, 2)
        loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=features['label']))
        is_correct = tf.equal(tf.argmax(logits, 1, output_type=tf.int32), features['label'])  # (N,)
        acc = tf.reduce_mean(tf.cast(is_correct, tf.float32)) # scalar
        return loss, acc

    def build_optimizer(self, features):
        loss, acc = self.build_loss_acc(features)
        # define optimizer
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        grad, var = zip(*optimizer.compute_gradients(loss))
        # clipping
        grad = [None if g is None else tf.clip_by_norm(g, 2.5) for g in grad]
        opt = optimizer.apply_gradients(zip(grad, var))
        return loss, acc, opt
