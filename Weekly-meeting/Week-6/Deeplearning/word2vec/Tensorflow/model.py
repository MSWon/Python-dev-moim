import tensorflow as tf


class Word2vec(object):
    def __init__(self, name, emb_dim, vocab_size, num_samples, use_clip, learning_rate, mode):
        self.name = name
        self.initializer = tf.random_uniform_initializer(-0.05, 0.05)
        self.emb_dim = emb_dim
        self.vocab_size = vocab_size
        self.num_samples = num_samples

        self.use_clip = use_clip
        self.learning_rate = learning_rate
        self.mode = mode

        self.inputs = tf.placeholder(tf.int32, shape=[None])
        self.labels = tf.placeholder(tf.int32, shape=[None])
        self._labels = tf.reshape(self.labels, [-1, 1])

        with tf.variable_scope(self.name):
            # Build graph
            self.build_graph()
            # Build optimizer & updater
            self.build_opt()

    def build_graph(self):

        # Embedding
        self.emb_w = self.get_var(name='emb_w', shape=[self.vocab_size, self.emb_dim])
        self.inputs_emb = tf.nn.embedding_lookup(self.emb_w, self.inputs)

        self.nce_w = self.get_var(name="nce_w", shape=[self.vocab_size, self.emb_dim])
        self.nce_b = self.get_var(name="nce_b", shape=[self.vocab_size])

        if self.mode == "nce":
            # NCE loss
            self.loss = tf.reduce_mean(
                tf.nn.nce_loss(weights=self.nce_w, biases=self.nce_b,
                            labels=self._labels,
                            inputs=self.inputs_emb,
                            num_sampled=self.num_samples,
                            num_classes=self.vocab_size))
        else:
            # Sampled softmax.
            self._labels = tf.reshape(self._labels, (-1, 1))
            self.loss = tf.reduce_mean(
                tf.nn.sampled_softmax_loss(weights=self.nce_w, biases=self.nce_b,
                            labels=self._labels,
                            inputs=self.inputs_emb,
                            num_sampled=self.num_samples,
                            num_classes=self.vocab_size))

    def build_opt(self):
        # define optimizer
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        grad, var = zip(*optimizer.compute_gradients(self.loss))

        # gradient clipping
        def clipped_grad(grad):
            return [None if g is None else tf.clip_by_norm(g, 2.5) for g in grad]

        if self.use_clip:
            grad = clipped_grad(grad)

        self.update = optimizer.apply_gradients(zip(grad, var))

    def get_var(self, name='', shape=None, dtype=tf.float32):
        return tf.get_variable(name, shape, dtype=dtype, initializer=self.initializer)

    def save(self, sess, global_step=None):
        var_list = [var for var in tf.all_variables() if self.name in var.name]
        saver = tf.train.Saver(var_list)
        save_path = saver.save(sess, save_path=f"model_{self.name}/w2v_model", global_step=global_step)
        print(' * model saved at \'{}\''.format(save_path))

    # Load whole weights
    def restore(self, sess):
        print(' - Restoring variables...')
        var_list = [var for var in tf.all_variables() if self.name in var.name]
        saver = tf.train.Saver(var_list)
        saver.restore(sess, f"model_{self.name}/w2v_model")
        print(' * model restored ')