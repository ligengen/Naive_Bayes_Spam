# Naive_Bayes_Spam
Tsinghua Introduction to machine learning proj.

* 首先运行process.py文件训练出模型，训练出的模型会存在本目录下的四个文件中
再运行nb.py在测试集上运行得到实验结果

* process.py文件的main函数中的GetBagOfWords函数的三个参数分别是：测试集的起始目录，测试集终止目录，sampling_rate，需要保证nb.py里的main函数的ss和ee两个值和"测试集的起始目录"以及“测试集的终止目录”相同。

* 实验用了five-fold。因为太懒所以没有shuffule。实验所有的要求都在Exp1NaiveBayesReadme里写了，数据集也可以在那里下载
