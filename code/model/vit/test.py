from efficientvit.cls_model_zoo import create_cls_model
import torch
from torchvision import transforms
from PIL import Image
model = create_cls_model(
  name="b1", weight_url="assets/checkpoints/cls/b1-r224.pt"
)
# 1. 加载图像
image_path1 = "dataset/imagenet/test/Grape Leaf Blight.JPG"
image_path2 = "dataset/imagenet/test/Grape_Black_rot.jpg"
image_path3 = "dataset/imagenet/test/Grape___Esca_(Black_Measles).jpg"
image_path4 = "dataset/imagenet/test/Grape_heathy.JPG"
image_path5 = "dataset/imagenet/test/Grapevine_yellow.jpg"
image = Image.open(image_path1).convert("RGB")

# 2. 图像预处理
preprocess = transforms.Compose([
    transforms.Resize((288, 288)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_image = preprocess(image)
input_batch = input_image.unsqueeze(0)  # 添加批量维度

# 3. 模型推断
with torch.no_grad():
    model.eval()
    output = model(input_batch)

# 4. 获取预测结果
probabilities = torch.nn.functional.softmax(output[0], dim=0)
predicted_class = torch.argmax(probabilities).item()

# 5. 打印结果
print(f"Predicted class: {predicted_class}")
#print(f"Class probabilities: {probabilities}")