import json

if __name__ == '__main__':
    with open("D:\\softwareInstall\\JianyingPro Drafts\\第一章\\draft_content.json", "r", encoding='utf-8') as f:
        json_str = f.read()
        # json_content = json.loads(json_str)
        # print(json_str)
        # texts_data = json_content["materials"]["texts"]
        # for text_data in texts_data:
        #     content = text_data["content"]
        #     content = content[:-22]
        #     result = content.split("><size=")[1].split(">")[1]
        #     print(result)
