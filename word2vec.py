from gensim.models import word2vec
import jieba
import jieba.posseg as pseg
import numpy as np
import pandas as pd


def get_words(data_path, sheet_name):
    df = pd.read_excel(data_path, sheet_name=sheet_name)

    words_list = []
    sentence_list = []
    polar_list = []
    for i in df.index:
        S = str(df.comment[i])
        S = S.replace('\n', '')
        # words = pseg.cut(S)
        words = jieba.cut(S)
        # temp_list用于存放句子中不同的word
        stemp_list = []
        ptemp_list = []
        for word in words:
            # 如果该词不在停用词典中，将其写入临时存储数组中，以便后续写入到sentence_list
            if word not in stopwords:
                words_list.append(word)
                stemp_list.append(word)
            # 如果该词在极性词典中，将其写入临时存储数组中，以便后续写入到polar_list
            if word in polarwords:
                ptemp_list.append(word)
        if len(stemp_list) > 5:
            sentence_list.append(stemp_list)
            if len(ptemp_list) > 0:
                polar_list.append(ptemp_list)

    return words_list, sentence_list, polar_list


def sim(s1, s2):
    similarity = model.wv.similarity(s1, s2)
    print('(' + s1 + ',' + s2 + ') ：' + str(similarity))
    return similarity


def count_word(sentence, cw):
    counts = {}
    for words in sentence:
        for word in words:
            if word in cw:
                counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    return items


data_path = '../comData/keep.xlsx'
jieba.load_userdict("userdict.txt")
stopwords = [line.strip() for line in open('stopWord.txt', encoding='UTF-8').readlines()]
polarwords = [line.strip() for line in open('polarword_new.txt', encoding='UTF-8').readlines()]

words_list, sentence_list, polar_list = get_words(data_path, 'total')
print('分词完成！')
# with open('sentenceList.txt', 'w') as f:
#     for sentence in sentence_list:
#         f.write(str('/'.join(sentence)) + "\n")

# 选择基准极性词basic word list
bword_list = [['不错', '糟糕'], ['满意', '失望'], ['喜欢', '差劲'], ['开心', '不满'], ['准确', '错误']]
# 创建游戏化元素记录
game_words = ['挑战', '活动', '任务', '训练营', '打卡', '徽章', '成就',
              '等级', '积分', '成长值', 'live模式', '语音', '排行', '排名',
              '社区', '社会', '日记', '动态', '角色', '现女友', '人物',
              '卡路里币', '卡路里工厂', '金币', '剧情跑']

game_word_list = [['挑战', '活动', '任务'], ['训练营'], ['打卡'], ['徽章'], ['成就'],
                  ['等级', '积分', '成长值'], ['live模式', '语音'], ['排行', '排名'],
                  ['社区', '社会'], ['日记', '动态'], ['角色', '现女友', '人物'],
                  ['卡路里币', '卡路里工厂'], ['金币', '剧情跑']]
# 可以用list[:]来访问内部的所有元素
# 建立学习模型
model = word2vec.Word2Vec(sentence_list, min_count=1)

# 计算每一条评论的极性值：
for comment in polar_list:
    # 单条评论的情感值，Tcom
    Tcom = 0
    for word in comment:
        # Tu 为单个极性词的极性值，算法为与每个所选定的基准极性词计算sim()
        Tu = 0
        if word not in game_words:
            for bword in bword_list:
                Tu += sim(word, bword[0]) - sim(word, bword[1])
        Tcom += Tu
    comment.append(str(Tcom))

# 计算每个游戏化元素的极性值，计算公式：含有游戏化元素的评论的情感值的平均值
# game_num_list为包含游戏化元素计数的列表
game_num_list = count_word(polar_list, game_words)
game_num_list2 = []
for game_word_comp in game_word_list:
    sum = 0
    for game_num in game_num_list:
        if game_num[0] in game_word_comp:
            sum += int(game_num[1])
    game_num_list2.append([game_word_comp, sum])



Tgame = []
for gamifacation in game_num_list2:
    # game_sum为包含游戏化元素的评论情感值的加和
    game_sum = 0
    for sentence in polar_list:
        hasgame = False
        for word in sentence:
            if word in gamifacation[0]:
                hasgame = True

        if hasgame is True:
            game_sum += float(sentence[-1])

    Tgame.append([gamifacation[0], game_sum/gamifacation[1]])

# 进行归一化处理：
emotion_list =[]
for T in Tgame:
    emotion_list.append(T[-1])
for T in Tgame:
    T[-1] = (T[-1] - min(emotion_list))/(max(emotion_list)-min(emotion_list))

print(Tgame)

# with open('polarList.txt', 'w') as f:
#     for sentence in polar_list:
#         hasgame = False
#         for word in sentence:
#             if word in game_words:
#                 hasgame = True
#                 break
#         if hasgame is True:
#             f.write(str('/'.join(sentence)) + "\n")



# sim('坚持', '训练')
# sim('坚持', '更新')
# sim('好用', '不好')

# res = model.wv.most_similar('好用')
# for r in res:
#     print(r[0],r[1])
