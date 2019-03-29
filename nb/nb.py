from __future__ import division
from data_process.process import ProcessEmail
from data_process.process import ProcessLabel
import json
import math
import time
import subprocess


class Nb(object):
    p_y = 0
    word_lis = []
    spam_total = 0
    ham_total = 0
    global spam_bag
    global ham_bag

    def __init__(self):
        # self.words_bag_train = json.loads(open('../words_bag_train', 'r').read())
        # self.words_bag_test = json.loads(open('../words_bag_test', 'r').read())
        self.spam_total = sum(spam_bag.values())
        self.ham_total = sum(ham_bag.values())
        self.email_obj = None

        self.label_obj = ProcessLabel()
        self.p_y = self.label_obj.get_prob()

    def init_email_obj(self, fir, sec):
        self.email_obj = ProcessEmail("%03d" % fir + '/%03d' % sec)

    def set_word_lis(self):
        text = self.email_obj.text
        tmp = []
        for line in text:
            for word in line.split():
                tmp.append(word)
        self.word_lis = tmp

    def calc_p_x_i_spam(self):
        ans = math.log(self.p_y)
        for word in self.word_lis:
            if word in spam_bag:
                ans += math.log(spam_bag[word] / self.spam_total)
            # laplace smoothing
            else:
                ans += math.log(laplace * 1.0 / self.spam_total + laplace * len(spam_bag))
            # Manually smoothing, if you want to test this part,
            # just uncomment this and comment above laplace
            '''elif word in ham_bag:
                ans += math.log(0.01)
            else:
                ans += math.log(0.4)'''
        return ans

    def calc_p_y_i_ham(self):
        ans = math.log(1 - self.p_y)
        for word in self.word_lis:
            if word in ham_bag:
                ans += math.log(ham_bag[word] / self.ham_total)
            else:
                ans += math.log(laplace * 1.0 / self.ham_total + laplace * len(ham_bag))
            '''elif word in spam_bag:
                ans += math.log(0.01)
            else:
                ans += math.log(0.4)'''
        return ans

    def ans_return(self):
        return self.calc_p_x_i_spam() > self.calc_p_y_i_ham()


class Evaluation(object):
    total = 0
    right = 0
    true_pos = 0
    false_neg = 0
    false_pos = 0
    true_neg = 0

    def __init__(self):
        self.label_obj = ProcessLabel()

    def evaluation(self, start, end):
        for i in range(start, end):
            print('begin testing file %03d/***' % i)
            max_ = 300
            if i == 215:
                max_ = 120
            for j in range(max_):
                if j % 50 == 0:
                    print('finish testing %03d/%03d' % (i, j))
                self.total += 1
                path = "%03d" % i + '/%03d' % j
                nb = Nb()
                nb.init_email_obj(i, j)
                nb.set_word_lis()
                predict = nb.ans_return()
                should_be = self.label_obj.label[path]
                if predict == should_be:
                    self.right += 1
                if should_be == 1:
                    if predict == 1:
                        self.true_pos += 1
                    else:
                        self.false_neg += 1
                else:
                    if predict == 1:
                        self.false_pos += 1
                    else:
                        self.true_neg += 1
            print('finish testing file %03d/***' % i)
        precision = self.true_pos / (self.true_pos + self.false_pos)
        recall = self.true_pos / (self.true_pos + self.false_neg)
        return self.right / self.total, precision, recall, 2 * precision * recall / (precision + recall)


if __name__ == "__main__":
    # 0-43 43-86 86-129 129-172 172-216
    time_sta = time.time()
    laplace = 1e-40
    eva = Evaluation()
    with open('../words_spam', 'r') as f:
        spam_bag = json.loads(f.read())
    f.close()
    with open('../words_ham', 'r') as f:
        ham_bag = json.loads(f.read())
    f.close()
    ss = 172
    ee = 216
    print('all data are kept in files.')
    acc, pre, recall, f1 = eva.evaluation(ss, ee)
    print('Accuracy of testing set from %03d/*** to %03d/*** is' % (ss, ee), acc)
    print('Precision of testing set from %03d/*** to %03d/*** is' % (ss, ee), pre)
    print('Recall of testing set from %03d/*** to %03d/*** is' % (ss, ee), recall)
    print('F1 of testing set from %03d/*** to %03d/*** is' % (ss, ee), f1)
    time_end = time.time()
    print('total time is: ', time_end - time_sta)
