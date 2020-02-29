import pandas as pd

def moim_stats(args):
    '''
    :param args: argparse
    :return: prints out statistics information of input text file
    '''
    file_path = args.input_path
    N = int(args.number)

    word_dic = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for sent in f:
            for word in sent.split():
                if word not in word_dic:
                    word_dic[word] = 1
                else:
                    word_dic[word] += 1

    N_word = sorted(word_dic.items(), key= lambda x: x[1], reverse=True)[:N]
    df_dic = {"word":[word for word,freq in N_word],
              "frequency":[freq for word,freq in N_word]}
    df_index = ["{}.".format(idx) for idx in range(1,N+1)]
    df = pd.DataFrame(df_dic, index=df_index)
    print("statistics for top {} frequent words in {}".format(N, file_path))
    print(df)
