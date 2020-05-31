# -*- coding: utf-8 -*-
import gensim
import re
import io
import jieba
import multiprocessing

class WordEmbedding():

    corpus_folder = r'/Users/rongyebei/Desktop/corpus'
    corpus_name = ['ChnSentiCorp', 'discussion', 'SogouC']
    punctuation = re.compile(u"[-~!@#$%^&*()_+`=\[\]\\\{\}\"|;':,./<>?·！@#￥%……&*（）——+【】、；‘：“”，。、《》？「『」』]")

    def preprocess(self, input_file, output_file):  # replace punctuation

        punctuation = re.compile(u"[-~!@#$%^&*()_+`=\[\]\\\{\}\"|;':,./<>?·！@#￥%……&*（）——+【】、；‘：“”，。、《》？「『」』]")

        with io.open(output_file, mode='w', encoding='utf-8') as outfile:
            with io.open(input_file, mode='rb') as infile:
                for line in infile:
                    # line = multi_version.sub(r'\2', line)
                    line = punctuation.sub(' ', line.decode('utf-8'))
                    outfile.write(line)

        print('========Preprocessing: Replaced punctuations with blank space')

    def train(self, input_file, output_file):
        sentences = gensim.models.word2vec.LineSentence(input_file)
        model = gensim.models.Word2Vec(sentences, size=100, min_count=10, workers=multiprocessing.cpu_count())
        model.save(output_file)
        # model.save_word2vec_format(output_file + '.vector', binary=True)

        print('Corpus has been trained.')

    def my_cut(self, input_file, output_file):

        with io.open(output_file, mode='w', encoding='utf-8') as outfile:
            with io.open(input_file, mode='r', encoding='utf-8') as infile:
                for line in infile:
                    line = self.punctuation.sub(' ', line)
                    # line = jieba.cut()
                    outfile.write(' '.join(list(jieba.cut(line))))
