# -*- coding: utf-8 -*-
# @Time    : 2021-05-18 14:08
# @Author  : prophet
# @Email   : liukeqiang99999@163.com
import base64
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json
import sys
import os.path

module_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(module_dir + '/../../lib/')
from tencent_ai_texsmart import *


engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

app = FastAPI()


class Item(BaseModel):
    item_id: str
    content: str
    kws_type: int
    ner_type: int


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/nlu/p/")
def read_item(item: Item):
    ner = {}
    leave1_word_list = []
    leave2_word_list = []
    text_matching = []
    related_list = []
    # content = str(base64.b64decode(item.content), 'utf-8')
    content = item.content
    item_id = item.item_id
    kws_type = item.kws_type
    ner_type = item.ner_type
    # print(item_id, kws_type == 1, ner_type == 1, content)
    output = engine.parse_text(content)
    if kws_type == 0:
        # print(u'细粒度分词: True')
        for item in output.words():
            tmp = {}
            tmp['str'] = item.str
            tmp['tag'] = item.tag
            leave1_word_list.append(tmp)
            # print(u'\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
    elif kws_type == 1:
        # print(u'粗粒度分词: True')
        for item in output.phrases():
            tmp = {}
            tmp['str'] = item.str
            tmp['tag'] = item.tag
            leave2_word_list.append(tmp)
            # print(u'\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
    if ner_type == 1:
        # print(u'命名实体识别（NER）:')
        # for entity in output.entities():
        #     type_str = u'({0},{1},{2},{3})'.format(entity.type.name, entity.type.i18n, entity.type.flag, entity.type.path)
        #     print(u'\t{0}\t({1},{2})\t{3}\t{4}'.format(entity.str, entity.offset, entity.len, type_str, entity.meaning))
        if len(output.entities()) > 0:
            for entity in output.entities():
                # try:
                tmp = {}
                word = entity.str
                offset = entity.offset
                lens = entity.len
                cl = entity.type.i18n
                tmp['str'] = word
                tmp['offset'] = offset
                tmp['len'] = lens
                tmp['tag'] = cl
                if entity.meaning == '':
                    tmp['related'] = ','.join([])
                else:
                    mp = eval(entity.meaning)
                    rel = mp.get('related', mp.get('value'))
                    tmp['related'] = rel
                # print(word, offset, lens, cl, rel)
                related_list.append(tmp)
        else:
            pass
    else:
        # print(u'=== Text Matching ===')
        output = engine.match_text(item_id, content)
        tmps = {}
        tmps['str1'] = item_id
        tmps['str2'] = content
        if output is None or output.size() < 1:
            # print(u'Error occurred in text matching')
            tmps['score'] = 'Error occurred in text matching'
        else:
            tmps['score'] = output.score_at(0)
        text_matching.append(tmps)
        # print(u'text1: {0}'.format(str1))
        # print(u'text2: {0}'.format(str2))
        # print(u'Matching score: {0}'.format(output.score_at(0)))

    ner['item_id'] = item_id
    ner['related_list'] = related_list
    ner['text_matching'] = text_matching
    ner['leave1_word_list'] = leave1_word_list
    ner['leave2_word_list'] = leave2_word_list
    # print(item_id,word_list,leave1_word_list,leave2_word_list)
    # nlu = json.dumps(ner, ensure_ascii=False)
    # print(nlu)
    return ner


@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    return {"item_name": item.content, "item_id": item_id}


"""
gunicorn api_nlu:app -b 0.0.0.0:8090 -w 6 -k uvicorn.workers.UvicornWorker --daemon 
pstree -ap|grep gunicorn
kill -HUP 30080
uvicorn api_nlu:app --host 0.0.0.0 --port 8090 --reload
curl -X GET '192.168.252.1:8090'
curl -H 'Content-Type:application/json' -X POST -d '{"item_id":123,"content":"产业大数据","kws_type":1,"ner_type":1}' 192.168.252.1:8090/nlu/p/
curl -H 'Content-Type:application/json' -X POST -d '{"item_id":456,"content":"腾讯减持Sea Limited 2.6%股权","kws_type":1,"ner_type":1}' 192.168.252.1:8090/nlu/p/
curl -H 'Content-Type:application/json' -X POST -d '{"item_id":789,"content":"肉豆蔻精油和罗勒精油在防治鸡坏死性肠炎中的应用","kws_type":1,"ner_type":1}' 192.168.252.1:8090/nlu/p/
"""
