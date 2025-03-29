import os
import json
import shutil

import pyJianYingDraft as draft
from pyJianYingDraft import trange, Outro_type
from . import __Jianying_path__, __comfyui_path__, __draft_path__, get_config


class JianYingDraft:

    def __init__(self, log_obj):
        self.log_info, self.log_success, self.log_fail, self.log_warn = log_obj
        self.script = draft.Script_file(1920, 1080)
        self.current_time = 0
        self.script.add_track(draft.Track_type.video).add_track(draft.Track_type.text)

    # 创建视频文件
    def video_create_copy(self, draft_name):
        source_folder = os.path.join(__Jianying_path__, "video_file", "default")
        destination_folder = os.path.join(__draft_path__, draft_name)
        try:
            if os.path.exists(destination_folder):
                shutil.rmtree(destination_folder)
            shutil.copytree(source_folder, destination_folder)
            self.log_success.emit(
                "成功将文件夹 " + source_folder + " 复制到 " + destination_folder)
        except FileNotFoundError:
            self.log_fail.emit("错误：源文件夹 " + source_folder + " 未找到。")
        except PermissionError:
            self.log_fail.emit("错误：没有权限复制文件夹到 " + destination_folder + "。")
        except Exception as e:
            self.log_fail.emit("发生未知错误：" + e)

    def add_image(self, image_path, time, text):
        sticker_material = draft.Video_material(__comfyui_path__ + image_path)
        self.script.add_material(sticker_material)  # 随手添加素材是好习惯

        sticker_segment = draft.Video_segment(sticker_material, trange(str(self.current_time) + "s", str(time) + "s"))
        self.script.add_segment(sticker_segment)

        # 创建一行类似字幕的文本片段并添加到轨道中
        text_segment = draft.Text_segment(text, trange(str(self.current_time) + "s", str(time) + "s"),
                                          # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                          font=draft.Font_type.文轩体,  # 设置字体为文轩体
                                          style=draft.Text_style(color=(1.0, 1.0, 0.0)),  # 设置字体颜色为黄色
                                          clip_settings=draft.Clip_settings(transform_y=-0.8))  # 模拟字幕的位置
        self.script.add_segment(text_segment)
        self.current_time += time

    def save_video(self, video_name):
        self.script.dump(__draft_path__ + video_name + "/draft_content.json")
        self.log_success.emit("【" + video_name + "】视频制作完成！")

    # 读取文件夹下所有.json文件的内容
    def read_json_files_from_folder(self):
        json_files = []
        for filename in os.listdir(__comfyui_path__):
            if filename.endswith('.json') and filename != 'prompt.json':
                json_files.append(filename)
        return json_files

    def start(self):
        if get_config()["jianying_draft"] == "":
            self.log_warn.emit("请先设置剪映草稿文件夹！")
            return

        if get_config()["jianying_draft_update"]:
            self.log_warn.emit("剪映草稿文件夹以修改，请重新启动软件！")
            return

        try:
            files = self.read_json_files_from_folder()
            for filename in files:
                self.video_create_copy(filename.replace('.json', ''))
                file_path = os.path.join(__comfyui_path__, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_content = json.load(file)
                    self.log_info.emit("正在制作【" + filename.replace('.json', '') + "】视频...")
                    for item in json_content["storyboard"]:
                        if item["image_path"] == "":
                            self.log_fail.emit("图片未生成,请先使用comfyui软件生成图片。")
                            break
                        self.add_image(item["image_path"], item["shot_time"], item["corresponding_text"])
                self.save_video(filename.replace('.json', ''))
        except Exception as e:
            self.log_fail.emit("视频自动剪辑时发生未知错误：" + e)
        self.log_success.emit("所有视频制作完成。")
