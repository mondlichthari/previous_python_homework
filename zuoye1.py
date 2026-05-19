import jieba
print(jieba.__file__)
from collections import Counter
import wordcloud
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from gensim import corpora, models

base_dir = os.path.dirname(__file__)
article_path = os.path.join(base_dir, "wbfx.txt")       # 文章文件
stopwords_path = os.path.join(base_dir, "停用词.txt")  # 停用词文件
mask_path = os.path.join(base_dir, "jumpingman.png")        # 词云形状图片
output_wordcloud = os.path.join(base_dir, "result2.png")  # 输出词云图片

with open(article_path, 'r', encoding="utf-8") as f:
    text = f.read()

stopwords = set()
with open(stopwords_path, 'r', encoding="utf-8") as f:
    content = [line.strip() for line in f.readlines()]
stopwords.update(content)

ls = jieba.lcut(text)
words = [w for w in ls if w not in stopwords and len(w) > 1]

word_counts = Counter(words)
top10 = word_counts.most_common(10)
print("出现次数最多的10个词：")
for word, count in top10:
    print(f"{word} {count}")

long_words_count = sum(1 for w in words if len(w) >= 4)
print(f"\n4个字以上（含4个）的词数量：{long_words_count}")

mask = imageio.imread(mask_path)
txt = " ".join(words)

w = wordcloud.WordCloud(
    font_path="msyh.ttc",
    mask=mask,
    width=1000,
    height=700,
    background_color="white",
    stopwords=stopwords
)
w.generate(txt)
w.to_file(output_wordcloud)

plt.imshow(w)
plt.axis('off')
plt.show()

documents = [words]
dictionary = corpora.Dictionary(documents)
corpus = [dictionary.doc2bow(doc) for doc in documents]

# LDA模型
num_topics = 3
lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=20)

print("\nLDA主题词：")
for i in range(num_topics):
    print(f"主题 {i+1}:")
    for word, prob in lda_model.show_topic(i, topn=10):
        print(f"{word} ({prob:.3f})", end="  ")
    print("\n")