# -*- coding: utf-8 -*-
from WordEmbedding import WordEmbedding
import os
import gensim


if __name__ == '__main__':

    word_embdedding = WordEmbedding()

    corpus_folder = word_embdedding.corpus_folder
    corpus_name = word_embdedding.corpus_name

    discussion_folder = corpus_folder + '/' + corpus_name[1]  # discussion
    discussion_file = os.listdir(discussion_folder)
    discussion_file = ['601933.txt', '000651.txt', '000725.txt', '603288.txt', '002252.txt', '601111.txt', '600025.txt', '002142.txt', '601229.txt', '600309.txt', '000568.txt', '600900.txt', '603993.txt', '002352.txt', '002024.txt', '601398.txt', '601601.txt', '601985.txt', '002027.txt', '601238.txt', '601166.txt', '601989.txt', '601988.txt', '601618.txt', '600276.txt', '600115.txt', '002415.txt', '601390.txt', '600028.txt', '600000.txt', '600606.txt', '002304.txt', '000895.txt', '601899.txt', '601669.txt', '000538.txt', '600010.txt']

    # for f in discussion_file:
    #
    #     word_embdedding.my_cut(discussion_folder + '/' + f, corpus_folder + r'/preprocessed_discussion/' + '{}'.format(f))
    #     print('File {0} written'.format(f))

    review_folder = corpus_folder + '/' + corpus_name[0] + '/negative'  # review neg
    review_file = os.listdir(review_folder)
    # review_file.pop(review_file.index('.DS_Store'))


    # for f in review_file:
    #     word_embdedding.my_cut(review_folder + '/' + f, corpus_folder + r'/cut_ChnSentiCorp/negative/' + '{}'.format(f))
    #
    # print('cut_ChnSentiCorp negative written down')

    review_folder = corpus_folder + '/' + corpus_name[0] + '/positive'  # review pos
    review_file = os.listdir(review_folder)
    # review_file.pop(review_file.index('.DS_Store'))

    # for f in review_file:
    #     word_embdedding.my_cut(review_folder + '/' + f, corpus_folder + r'/cut_ChnSentiCorp/positive/' + '{}'.format(f))
    #
    # print('cut_ChnSentiCorp positive written down')

    #word_embdedding.train(corpus_folder + '/gensim_corpus/merge_corpus.txt', corpus_folder + '/Word2Vec/embedding.txt')

    model = gensim.models.Word2Vec.load(corpus_folder + '/Word2Vec/embedding.txt')





