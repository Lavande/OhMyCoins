import jieba


def stopwordslist(filepath):
    # 停用词表
    f = open(filepath, 'r', encoding='utf-8')
    stopwords = [d.strip() for d in f.readlines()]
    f.close()
    return stopwords


def cutWords(sentence, stopwords):
    # 分词
    custom_words = ['以太坊','比特币','区块链','去中心化','新领域']
    for i in custom_words: jieba.add_word(i)
    seg_list = jieba.cut(sentence)
    results = []
    words = " ".join(seg_list).split(' ')
    for w in words:
        if w not in stopwords:
            results.append(w)
    return results


def parseData():
    stopwords = stopwordslist('stopwords.txt')
    words = {}
    with open('blockchain_news', encoding='utf-8') as f:
        data = f.readlines()
        for d in data:
            results = cutWords(d[:-1], stopwords)
            for r in results:
                if r in words:
                    words[r] += 1
                else:
                    words[r] = 1
    finals = {}
    for w in words:
        if words[w] > 200:
            finals[w] = words[w]
    return finals


if __name__ == '__main__':
    results = parseData()
    for r in results:
        print(r, results[r])
