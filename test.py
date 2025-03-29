from gtts import gTTS
from nltk.tokenize import sent_tokenize, word_tokenize
# 读取文本文件
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
# 处理文本内容
def process_text(text):
    # 分句
    sentences = sent_tokenize(text)
    # 分词
    words = word_tokenize(text)
    return sentences, words
# 将处理后的文本转换为语音
def convert_to_speech(text):
    tts = gTTS(text=text, lang='zh')
    tts.save("output.mp3")
    print("语音已生成，请查看输出文件。")

# 主函数
def main():
    # file_path = input("请输入文本文件路径：")
    text = read_text_file("D:\\Code\\PyCharmCode\\pyusewindows\\is_ai_article_data\\abc.txt")
    sentences, words = process_text(text)
    for sentence in sentences:
        convert_to_speech(sentence)

if __name__ == '__main__':
    main()
