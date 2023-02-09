RUN pip install --index-url https://pypi.douban.com/simple --default-timeout=100 --no-cache-dir -r /code/requirements.txt
docker build -t text_understanding_api .

curl -X GET '192.168.252.1:8090'

kws_type:1 粗粒度分词 kws_type:0 细粒度分词
ner_type:1 开启实体识别 0 开启文本相似度匹配
curl -H 'Content-Type:application/json' -X POST -d '{"item_id":"大数据","content":"产业大数据","kws_type":1,"ner_type":1}' 192.168.252.1:8090/nlu/p/
