import os
import json
"""
遍历当前目录，合并json文件
"""
if __name__ == "__main__":
    res = []
    for _, _, file in os.walk(os.path.dirname(os.path.abspath(__file__))):
        for f in file:
            if f.endswith('.json'):
                with open(f, 'r', encoding='utf8') as f_r:
                    # res.append(json.loads(f_r.read()))  #
                    # res += json.loads(f_r.read())  #
                    pass
    # with open('船舶状态查询.json', 'w', encoding='utf8') as f_w:
    #     f_w.write(json.dumps(res, ensure_ascii=False))
    # with open('船舶状态查询-中文.json', 'w', encoding='utf8') as f_w:
    #     f_w.write(json.dumps(res, ensure_ascii=False))
