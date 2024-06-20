import streamlit as st  # 导入Streamlit库，用于构建Web应用
import jieba  # 导入jieba库，用于中文分词
import requests  # 导入requests库，用于发送网络请求
from collections import Counter  # 从collections模块导入Counter类，用于词频统计
import re  # 导入正则表达式库
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML
import matplotlib.pyplot as plt  # 导入matplotlib的pyplot模块，用于绘图
import pandas as pd  # 导入pandas库，用于数据处理
from wordcloud import WordCloud  # 导入wordcloud模块中的WordCloud类

# 配置matplotlib以支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']

# 定义一个函数，用于清理HTML文本
def clean_text(text):
    soup = BeautifulSoup(text, "html.parser")  # 使用BeautifulSoup解析HTML
    text = soup.get_text()  # 提取文本内容
    text = re.sub(r'\s+', '', text)  # 使用正则表达式移除多余的空白字符
    return text

# 定义一个函数，用于去除文本中的标点符号和数字
def remove_punctuation_and_numbers(text):
    text = re.sub(r'[^\w\s]', '', text)  # 移除非字母数字和下划线的字符
    text = re.sub(r'\d+', '', text)  # 移除数字
    return text

# 定义一个函数，用于分词并去除停用词
def segment(text):
    stopwords = ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '之', '与', '和', '或']
    text = remove_punctuation_and_numbers(text)  # 先去除标点和数字
    words = jieba.lcut(text)  # 使用jieba进行分词
    words = [word for word in words if word and word not in stopwords]  # 去除空字符串和停用词
    return words

# 定义主函数
def main():
    st.title("文本分析与词云可视化")  # 设置应用标题

    # 创建一个文本输入框，让用户输入网页URL
    url = st.text_input("请输入网页 URL:")

    # 如果用户输入了URL
    if url:
        # 发送GET请求获取网页内容
        response = requests.get(url)
        response.encoding = 'utf-8'  # 设置编码为utf-8
        text = response.text  # 获取响应的文本内容

        # 清理文本
        text = clean_text(text)
        # 分词
        words = segment(text)
        # 统计词频
        word_counts = Counter(words)
        # 获取词频最高的20个词
        top_words = dict(word_counts.most_common(20))

        # 生成词云
        wordcloud = WordCloud(font_path='SimHei.ttf', max_words=20).generate_from_frequencies(top_words)

        # 绘制并显示词云图
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')  # 使用imshow显示词云
        plt.axis("off")  # 不显示坐标轴
        st.pyplot(plt)  # 使用Streamlit显示图表

        # 创建DataFrame展示词频统计
        top_words_df = pd.DataFrame(list(top_words.items()), columns=['词语', '词频'])
        # 添加序号列
        top_words_df['序号'] = range(1, 21)

        # 绘制横向柱状图
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(top_words_df['词语'], top_words_df['词频'], color='skyblue')  # 绘制柱状图
        ax.set_xticklabels(top_words_df['词语'], rotation=45, ha="right")  # 设置x轴标签
        ax.set_xlabel('词语')  # 设置x轴标题
        ax.set_ylabel('词频')  # 设置y轴标题
        ax.set_title('前20个词频统计条形图')  # 设置图表标题

        # 显示柱状图
        st.pyplot(fig)

        # 显示词频统计表格
        st.write("以下是前20个词频统计表格：")
        st.table(top_words_df)  # 使用Streamlit显示表格

# 确保当脚本被直接运行时，调用main函数
if __name__ == "__main__":
    main()
