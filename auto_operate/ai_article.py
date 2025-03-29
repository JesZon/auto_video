from . import __ai_article_path__, __comfyui_path__, client
import os
import json


class AIArticle:

    def __init__(self, log_obj):
        self.log_info, self.log_success, self.log_fail, self.log_warn = log_obj
        file_path = f"{__ai_article_path__}\\ai_cue_word.txt"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.prompt = f.read()
        except FileNotFoundError as e:
            self.log_fail.emit("错误：文件 ai_cue_word.txt 未找到：" + str(e))
        except Exception as e:
            self.log_fail.emit("发生未知错误：" + str(e))

    # 通过ai将用户的输入转换为comfyui的图片生成参数
    def open_ai_answer(self, user_prompt, file_name):
        pass
        self.log_info.emit("正在使用AI生成 " + file_name + " 的comfyui参数...")
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )
        convert = json.loads(response.choices[0].message.content)

        self.log_info.emit("生成【" + file_name + "】的comfyui参数完成!")
        self.save_json_to_file(convert, file_name.replace('.txt', ''))

    # 读取文件夹下所有的txt文件
    def read_files(self):
        self.log_info.emit("读取文件列表中...")

        file_list = []
        for file in os.listdir(__ai_article_path__):
            if file.endswith('.txt') and file != 'ai_cue_word.txt':
                file_list.append(file)

        self.log_info.emit("读取文件列表完成!")
        return file_list

    # 读取文件内容
    def read_file(self, file):
        self.log_info.emit("读取文件【" + file + "】中的内容...")
        file_path = f"{__ai_article_path__}\\{file}"
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.log_info.emit("文件【" + file + "】的内容读取完毕!")
            return content

    # 保存json数据到文件
    def save_json_to_file(self, json_data, file_name):
        # 将响应的json数据导出到文件中
        self.log_info.emit("开始保存【" + file_name + ".txt】的comfyui参数到【" + file_name + ".json】文件中...")
        with open(__comfyui_path__ + '\\' + file_name + ".json", 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
            self.log_info.emit("文件【" + file_name + ".json】保存成功!")

    # 正式操作执行
    def ai_article_main(self):
        if self.prompt:
            file_list = self.read_files()
            for file_name in file_list:
                self.open_ai_answer(self.read_file(file_name), file_name)
            self.log_success.emit("ai文章转图片参数进程结束，全部任务已完成！")
        else:
            self.log_fail.emit("任务结束，请修复错误后重试！")
