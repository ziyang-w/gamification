# gamification
本仓库用于存放大创期间所应用的代码，因为初学并且时间有限，所以python的代码编写比较粗糙，望见谅，等后续论文发表后会将数据上传

主要有如下内容：

1. polarword.txt，为极性词表，来源于[知网hownet](http://www.keenage.com/html/c_index.html)，我们将其中列举的中文常用的极性词进行了整理，得到了适用于网上评论的极性词表。
2. stopword.txt，最初来源是GitHub上的一个[停用词表](https://github.com/goto456/stopwords)中的百度停用词表。之后我们根据自身的评论中的特征加入了一些明星的名字以及一些我们不希望出现在最后分词结果中的词语
3. userdict.txt，是在jieba分词库中根据情况自己添加的词表。
4. word2vec.py，主要是大创期间分词和情感值计算，以及归一化游戏化元素极性值的py文件。其中引用到的数据文件会在之后研究结束后上传，并且会根据笔者的学习逐步完善。


# 引用

如果您对我们的研究感兴趣，请参考下面这篇文献。

[Impact of gamification elements on user satisfaction in health and fitness applications: A comprehensive approach based on the Kano model](https://doi.org/10.1016/j.chb.2021.107106)
