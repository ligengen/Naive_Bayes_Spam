# coding=utf-8
from __future__ import division
import json
import re
import random
import sys


class ProcessEmail(object):
    path = '../trec06c-utf8/data_cut/'
    total = ''
    text = []
    other_info = ''

    def __init__(self, path):
        self.path += path
        self.file = open(self.path, 'r')
        self.total = self.file.read()
        self.file.close()
        self.other_info = self.total.split('\n\n')

        reg = re.compile(u'[\s\u4E00-\u9FA5]+')
        tmp = []
        for i in self.other_info[1:]:
            tmp.extend(re.findall(reg, i))
        self.text = tmp

        reg = re.compile(u'http')
        tmp = []
        for i in self.other_info[1:]:
            tmp.extend(re.findall(reg, i))
        self.text.extend(tmp)

        regex = u'From.*@.*'
        pattern = re.compile(regex, re.I)
        from_text = re.findall(pattern, self.other_info[0])
        tmp = []
        if len(from_text) != 0:
            mails = from_text[0].split('@')[-1].split('>')[0].split(' ')[0]
            tmp.append(mails)
        self.text.extend(tmp)
        # print(self.text)
        # self.text = self.other_info[1:]
        self.other_info = self.other_info[0]


class ProcessLabel(object):
    label = {}
    num_1 = 0
    num_total = 0

    def __init__(self):
        self.file = open('../trec06c-utf8/label/index', 'r')
        total = self.file.readlines()
        for i in total:
            if 'spam' in i:
                str_ = i[13:20]
                self.label[str_] = 1
                self.num_1 += 1
            else:
                str_ = i[12:19]
                self.label[str_] = 0
            self.num_total += 1
        self.file.close()

    def get_label(self, fir, sec):
        return self.label["%03d" % fir + "/%03d" % sec]

    def get_prob(self):
        return self.num_1 / self.num_total

    def get_spam_num(self):
        return self.num_1

    def get_ham_num(self):
        return self.num_total - self.num_1


class GetBagOfWords(object):
    words_bag_train = {}
    words_bag_test = {}
    words_bag_spam = {}
    words_bag_ham = {}
    sampling_rate = 0

    def __init__(self, label_obj, start, end, sampling_rate):
        self.label_obj = label_obj
        self.start = start
        self.end = end
        self.sampling_rate = sampling_rate

    def from_text_get_word_bag(self, obj, spam, train=True):
        text = obj.text
        for line in text:
            for word in line.split():
                if train is True:
                    if random.random() < self.sampling_rate:
                        if word not in self.words_bag_train:
                            self.words_bag_train[word] = 1
                        else:
                            self.words_bag_train[word] += 1

                        if spam == 1:
                            if word not in self.words_bag_spam:
                                self.words_bag_spam[word] = 1
                            else:
                                self.words_bag_spam[word] += 1
                        else:
                            if word not in self.words_bag_ham:
                                self.words_bag_ham[word] = 1
                            else:
                                self.words_bag_ham[word] += 1
                    else:
                        pass
                else:
                    if word not in self.words_bag_test:
                        self.words_bag_test[word] = 1
                    else:
                        self.words_bag_test[word] += 1

    def get_bag_of_words(self):
        for i in range(self.start, self.end):
            if i % 10 == 0:
                print('......Processing test file %03d/***' % i)
            if i == 215:
                for j in range(120):
                    path = "215/" + "%03d" % j
                    self.from_text_get_word_bag(ProcessEmail(path), None, train=False)
            else:
                for j in range(300):
                    path = "%03d" % i + "/%03d" % j
                    self.from_text_get_word_bag(ProcessEmail(path), None, train=False)

        for i in range(0, self.start):
            if i % 10 == 0:
                print('......Processing train file %03d/***' % i)
            for j in range(300):
                path = "%03d" % i + "/%03d" % j
                self.from_text_get_word_bag(ProcessEmail(path), self.label_obj.get_label(i, j), train=True)

        for i in range(self.end, 216):
            if i % 10 == 0:
                print('......Processing train file %03d/***' % i)
            if i == 215:
                for j in range(120):
                    path = "215/" + "%03d" % j
                    self.from_text_get_word_bag(ProcessEmail(path), self.label_obj.get_label(i, j), train=True)
            else:
                for j in range(300):
                    path = "%03d" % i + "/%03d" % j
                    self.from_text_get_word_bag(ProcessEmail(path), self.label_obj.get_label(i, j), train=True)

    def print_words_bag_to_file(self):
        with open('../words_bag_train', 'w') as f:
            f.write(json.dumps(self.words_bag_train, ensure_ascii=False))
        f.close()
        with open('../words_spam', 'w') as f:
            f.write(json.dumps(self.words_bag_spam, ensure_ascii=False))
        f.close()
        with open('../words_ham', 'w') as f:
            f.write(json.dumps(self.words_bag_ham, ensure_ascii=False))
        f.close()
        with open('../words_bag_test', 'w') as f:
            f.write(json.dumps(self.words_bag_test, ensure_ascii=False))
        f.close()


if __name__ == "__main__":
    # 0-43 43-86 86-129 129-172 172-216
    print('spam email number: %d' % ProcessLabel().get_spam_num())
    a = GetBagOfWords(ProcessLabel(), 172, 216, 1)
    a.get_bag_of_words()
    a.print_words_bag_to_file()
