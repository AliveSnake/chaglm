FROM python:3.10

WORKDIR /chatglm

COPY requirements.txt .
RUN pip install -U pip 
RUN pip install -r requirements.txt 

COPY . .

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip install torchpack timm onnx onnxsim onnxruntime
RUN pip install -r requirements_2.txt 

# 在容器内运行 Django 服务
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
