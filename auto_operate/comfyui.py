import json
import websocket
import uuid
import urllib.request
import urllib.parse
import os
import random
import time

from . import __comfyui_path__, __comfyui_localhost__, __lens_batch__


class ComfyUI:

    # 初始化
    def __init__(self, log_obj):
        self.log_info, self.log_success, self.log_fail, self.log_warn = log_obj
        self.client_id = str(uuid.uuid4())
        self.seed = random.randint(1, 10000)
        self.working = f"{__comfyui_path__}\\prompt.json"
        self.image_path = f"{__comfyui_path__}\\images"
        self.positive = None
        self.negative = None

        try:
            self.ws = websocket.WebSocket()
            self.ws.connect("ws://{}/ws?clientId={}".format(__comfyui_localhost__, self.client_id))
            time.sleep(2)
            self.log_success.emit("正在建立websocket连接----")
            self.log_success.emit("客户端id：" + self.client_id + "\tseed：" + str(self.seed))
            self.log_success.emit("成功建立websocket连接！")
        except Exception as e:
            self.log_fail.emit("建立websocket连接失败！请查看comfyui服务是否启动！")
            self.log_fail.emit(str(e))

    def setPositive(self, positive):
        self.positive = positive

    def setNegative(self, negative):
        self.negative = negative

    def closeWS(self):
        if self.ws is not None:
            self.ws.close()

    # 定义一个函数向服务器队列发送提示信息
    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request("http://{}/prompt".format(__comfyui_localhost__), data=data)
        return json.loads(urllib.request.urlopen(req).read())

    # 定义一个函数来获取图片
    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(__comfyui_localhost__, url_values)) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(__comfyui_localhost__, prompt_id)) as response:
            return json.loads(response.read())

    # 定义一个函数来获取图片，这涉及到监听WebSocket消息
    def get_images(self, prompt):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_images = {}
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # 执行完成
            else:
                continue  # 预览为二进制数据
        history = self.get_history(prompt_id)[prompt_id]
        for _ in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                # 图片分支
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        images_output.append(image_data)
                    output_images[node_id] = images_output
                # 视频分支
                if 'videos' in node_output:
                    videos_output = []
                    for video in node_output['videos']:
                        video_data = self.get_image(video['filename'], video['subfolder'], video['type'])
                        videos_output.append(video_data)
                    output_images[node_id] = videos_output
        return output_images

    # 解析工作流并获取图片
    def parse_workflow(self):
        with open(self.working, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
            prompt_data = json.load(workflow_api_txt2gif_file)
            for node_id, node_data in prompt_data.items():
                if "inputs" in node_data and ("seed" in node_data["inputs"]
                                              or "value" in node_data["inputs"]
                                              or "last_seed" in node_data["inputs"]):
                    # 修改参数
                    if "seed" in node_data["inputs"]:
                        prompt_data[node_id]["inputs"]["seed"] = self.seed
                    if "value" in node_data["inputs"]:
                        prompt_data[node_id]["inputs"]["value"] = self.seed
                    if "last_seed" in node_data["inputs"]:
                        prompt_data[node_id]["inputs"]["seed"] = self.seed - 1
                if "inputs" in node_data and ("positive" in node_data["inputs"] or "negative" in node_data["inputs"]):
                    if not self.positive is None or not self.negative is None:
                        if "positive" in node_data["inputs"]:
                            prompt_data[node_id]["inputs"]["positive"] = self.positive
                        if "negative" in node_data["inputs"]:
                            prompt_data[node_id]["inputs"]["negative"] = self.negative
                    else:
                        self.log_warn.emit("未设置正反向提示词！跳出当前图片生成节点！")
                        return None

            return self.get_images(prompt_data)

    # 生成图像并显示
    def generate_clip(self, filename, item, index):
        images = self.parse_workflow()
        for node_id in images:
            for image_data in images[node_id]:
                GIF_LOCATION = "{}/{}_{}_{}.png".format(self.image_path, filename.rsplit('.', 1)[0], item["shot_id"],
                                                        index)
                with open(GIF_LOCATION, "wb") as binary_file:
                    # 写入二进制文件
                    binary_file.write(image_data)
                    item["image_path"] = "/images/{}_{}_{}.png".format(filename.rsplit('.', 1)[0], item["shot_id"],index)
                    self.log_info.emit("图片保存成功：" + GIF_LOCATION)

    # 读取文件夹下所有.json文件的内容
    def read_json_files_from_folder(self):
        self.log_info.emit("开始扫描参数文件夹...")
        json_files = []
        for filename in os.listdir(__comfyui_path__):
            if filename.endswith('.json') and filename != 'prompt.json':
                json_files.append(filename)
        return json_files

    def start_drawing(self, filename):
        self.log_info.emit("开始对【" + filename.rsplit('.', 1)[0] + "】进行图片生成...")
        file_path = os.path.join(__comfyui_path__, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
            for item in json_content["storyboard"]:
                # 设置正反向提示词
                self.setPositive(item["positive_prompt_words"])
                self.setNegative(item["reverse_prompt_words"])

                # 循环镜头批次
                for index in range(__lens_batch__):
                    self.generate_clip(filename, item, index + 1)
                    self.seed += 1
                    time.sleep(2)

                self.log_info.emit(
                    "【" + filename.rsplit('.', 1)[0] + "】的镜头 " + str(item["shot_id"]) + " 图片生成完毕...")

                self.setPositive(None)
                self.setNegative(None)

        # 导出修改后的 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_content, file, ensure_ascii=False, indent=4)

    def comfyui_main(self):
        if self.ws.connected:
            self.log_info.emit("开始生成图片...")
            if not os.path.exists(self.image_path):
                os.makedirs(self.image_path)
                self.log_info.emit("文件夹" + self.image_path + "不存在。")
                self.log_info.emit("成功创建" + self.image_path + "文件夹。")
            json_files = self.read_json_files_from_folder()
            for json_file in json_files:
                self.start_drawing(json_file)
                self.log_info.emit("【" + json_file.rsplit('.', 1)[0] + "】的图片全部生成完毕！")
            self.closeWS()
            self.log_success.emit("任务结束，完成comfyui图片生成！")
        else:
            self.log_fail.emit("任务结束，请修复错误后重试！")
