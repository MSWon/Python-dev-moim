import tensorflow as tf

_buffer_size = 20000
_bucket_size = 10
_thread_num = 16


def get_vocab(vocab_path, isTF=True):
    if isTF:
        vocab_path_tensor = tf.constant(vocab_path)
        tf.add_to_collection(tf.GraphKeys.ASSET_FILEPATHS, vocab_path_tensor)
        vocab_dict = tf.contrib.lookup.index_table_from_file(
            vocabulary_file=vocab_path_tensor,
            num_oov_buckets=0,
            default_value=1)
    else:
        vocab_dict = {}
        with open(vocab_path, "r") as f:
            for vocab in f:
                vocab_dict[len(vocab_dict)] = vocab.strip()
    return vocab_dict


def dataset_fn(corpus_path, vocab_path, max_len, batch_size):

  with tf.device("/cpu:0"):
      tf_vocab = get_vocab(vocab_path)
      dataset = tf.data.TextLineDataset(corpus_path)

      dataset = dataset.apply(tf.data.experimental.shuffle_and_repeat(_buffer_size))

      dataset = dataset.map(lambda x: tf.string_split([x], delimiter="\t").values)

      dataset = dataset.map(lambda x: {
                                "input": tf.string_split([x[0]]).values,
                                "label": tf.string_split([x[1]]).values
                            },
                            num_parallel_calls=_thread_num
                            )

      # Truncate to max_len
      dataset = dataset.map(lambda x:
                    tf.cond(tf.greater(tf.shape(x["input"])[0], max_len),
                            lambda: {
                                "input": x["input"][:max_len],
                                "label": x["label"]
                            },
                            lambda: {
                                "input": x["input"],
                                "label": x["label"]
                            }
                        )
                    )

      dataset = dataset.map(lambda x: {
                                "input": tf_vocab.lookup(x["input"]),
                                "label": x["label"]
                            },
                            num_parallel_calls=_thread_num
                            )

      dataset = dataset.map(lambda x: {
                                "input": tf.to_int32(x["input"]),
                                "seq_len": tf.shape(x["input"])[0],
                                "label": tf.strings.to_number(x["label"][0], tf.int32)
                            },
                                num_parallel_calls=_thread_num
                            )

      dataset = dataset.padded_batch(
          batch_size,
          {
              "input": [tf.Dimension(max_len)],
              "seq_len": [],
              "label": []
          },
          {
              "input": 0,
              "seq_len": 0,
              "label": 0
          }
      )

      # Prefetch the next element to improve speed of input pipeline.
      dataset = dataset.prefetch(3)
  return dataset



