import tensorflow as tf
from util import dataset_fn
from dense_model import Model


TRAIN_CORPUS_PATH = './data/ratings_train.cleaned.txt'
TEST_CORPUS_PATH = './data/ratings_test.cleaned.txt'
VOCAB_PATH = 'Word2vec.vocab'
VOCAB_MODEL_PATH = 'Word2vec.model'
MODEL_PATH = 'Dense.model'

MAX_LEN = 100
BATCH_SIZE = 128
LEARNING_RATE = 0.001
TRAIN_STEPS = 10000

#  Define placeholder
x = tf.placeholder(shape=(None, MAX_LEN), dtype=tf.int32)
seq_len = tf.placeholder(shape=(None,), dtype=tf.int32)
y = tf.placeholder(shape=(None,), dtype=tf.int32)

train_dataset = dataset_fn(TRAIN_CORPUS_PATH, VOCAB_PATH, MAX_LEN, BATCH_SIZE)
test_dataset = dataset_fn(TEST_CORPUS_PATH, VOCAB_PATH, MAX_LEN, BATCH_SIZE)

iters = tf.data.Iterator.from_structure(train_dataset.output_types,
                                        train_dataset.output_shapes)
features = iters.get_next()

# create the initialisation operations
train_init_op = iters.make_initializer(train_dataset)
test_init_op = iters.make_initializer(test_dataset)

print("Now building model")
model = Model(VOCAB_MODEL_PATH, MAX_LEN, LEARNING_RATE)
loss, acc, opt = model.build_optimizer(features)

# For Tensorboard

## for tensorboard
train_loss_graph = tf.placeholder(shape=None, dtype=tf.float32)
train_acc_graph = tf.placeholder(shape=None, dtype=tf.float32)
test_loss_graph = tf.placeholder(shape=None, dtype=tf.float32)
test_acc_graph = tf.placeholder(shape=None, dtype=tf.float32)

print("Now training")

saver = tf.train.Saver()
ckpt = tf.train.get_checkpoint_state("./model")

summary_train_loss = tf.summary.scalar("train_loss", train_loss_graph)
summary_train_acc = tf.summary.scalar("train_acc", train_acc_graph)
summary_test_loss = tf.summary.scalar("test_loss", test_loss_graph)
summary_test_acc = tf.summary.scalar("test_acc", test_acc_graph)
merged_train = tf.summary.merge([summary_train_loss, summary_train_acc])
merged_test = tf.summary.merge([summary_test_loss, summary_test_acc])

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    sess.run(train_init_op)
    sess.run(tf.tables_initializer())

    n_train_step = 0
    train_loss_, train_acc_ = 0., 0.
    test_loss_, test_acc_ = 0., 0.
    best_loss = 1e8
    writer = tf.summary.FileWriter('./tensorboard/graph', sess.graph)

    for step in range(TRAIN_STEPS):
        n_train_step += 1
        batch_train_loss, batch_train_acc, _ = sess.run([loss, acc, opt])
        train_loss_ += batch_train_loss
        train_acc_ += batch_train_acc
        train_loss = train_loss_ / n_train_step
        train_acc = train_acc_ / n_train_step

        print(f"step: {step + 1} train_loss: {train_loss} train_acc: {train_acc}")

        if step % 100 == 0 and step > 0:
            summary = sess.run(merged_train,
                               feed_dict={train_loss_graph: train_loss, train_acc_graph: train_acc})
            writer.add_summary(summary, step)

        if step % 2000 == 0 and step > 0:
            print("Now for test data")
            sess.run(test_init_op)
            n_test_step = 0

            try:
                while True:
                    n_test_step += 1
                    batch_test_loss, batch_test_acc = sess.run([loss, acc])
                    test_loss_ += batch_test_loss
                    test_acc_ += batch_test_acc

            except tf.errors.OutOfRangeError:
                pass

            test_loss = test_loss_ / n_test_step
            test_acc = test_acc_ / n_test_step

            summary = sess.run(merged_test, feed_dict={test_loss_graph: test_loss, test_acc_graph: test_loss})
            writer.add_summary(summary, step)
            print(f"step: {step + 1} test_loss: {test_loss} test_acc: {test_acc}")

            if test_loss < best_loss or step % 2000 == 0:
                save_path = saver.save(sess, "./model/" + MODEL_PATH)
                best_loss = test_loss

            sess.run(train_init_op)