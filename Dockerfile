# 1、从官方 Python 基础镜像开始
# FROM python:3.9
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# 2、将当前工作目录设置为 /code
# 这是放置 requirements.txt 文件和应用程序目录的地方
# WORKDIR /code
WORKDIR /app

# 3、先复制 requirements.txt 文件
# 由于这个文件不经常更改，Docker 会检测它并在这一步使用缓存，也为下一步启用缓存
# COPY ./requirements.txt /code/requirements.txt
COPY ./requirements.txt /app/requirements.txt

# 4、运行 pip 命令安装依赖项
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 5、复制 FastAPI 项目代码
# COPY ./app /code/app
COPY ./app /app

# 6、运行服务
# CMD ["uvicorn", "texsmart.examples.python.api_nlu:app", "--host", "0.0.0.0", "--port", "8090"]
# CMD ["gunicorn", "texsmart.examples.python.api_nlu:app", "-b", "0.0.0.0:8090", "-w", "2", "-k","uvicorn.workers.UvicornWorker"]
