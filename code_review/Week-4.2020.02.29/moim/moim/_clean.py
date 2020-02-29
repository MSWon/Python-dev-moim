import re

def prepro(sent):
    ''' preprocessing sentence (removing special symbols, replacing url with <URL> token)
    :param sent: input sentence (ex: I go to school)
    :return: cleaned sentence
    '''
    sent = re.sub("\(.*?\)|\[.*?\]", "", sent)
    sent = re.sub("[^0-9a-zA-Z가-힣_\-@\.:&+!?'/,\s]", "", sent)
    sent = re.sub("(http[s]?://([a-zA-Z]|[가-힣]|[0-9]|[-_@\.&+!*/])+)|(www.([a-zA-Z]|[가-힣]|[0-9]|[-_@\.&+!*/])+)", "<URL>", sent)
    return sent

def moim_clean(args):
    '''
    :param args: argparse
    :return: saves cleaned text
    '''
    file_path = args.input_path
    save_path = args.output_path

    f_input = open(file_path, "r", encoding="utf-8")

    with open(save_path, "w", encoding="utf-8") as f_output:
        for sent in f_input:
            f_output.write(prepro(sent))

    print("cleaning finished")