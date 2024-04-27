FROM python:3.10

WORKDIR /chatglm

COPY requirements.txt .
RUN pip install -U pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install torchpack timm onnx onnxsim onnxruntime -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements_2.txt -i https://mirrors.aliyun.com/pypi/simple/

# 在容器内运行 Django 服务
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
