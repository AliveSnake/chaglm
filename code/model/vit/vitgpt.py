#vit
import torch
from torchvision import transforms
from PIL import Image
import os
import json
import sys
from .model import resnet101
import torch.nn as nn

# gpt
from transformers import AutoTokenizer, AutoModel

#resnet
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
current_directory = os.path.dirname(__file__)

resNet_path = '/mnt/nas/resNet101y.pth'
chatglm_path = '/mnt/nas/freezeglm10'
# 检查路径是否存在
if not os.path.exists(resNet_path) or not os.path.exists(chatglm_path):
    # 如果路径不存在，则使用备用路径
    resNet_path = 'D:/FireFoxDownloads/resNet101y.pth'
    chatglm_path = 'D:/Models/ChatGLM3/freezeglm10'

# create model
cls_model = resnet101(num_classes=52).to(device)

# load model weights
weights_path = resNet_path
assert os.path.exists(weights_path), "file: '{}' does not exist.".format(weights_path)
cls_model.load_state_dict(torch.load(weights_path, map_location=device))

#gpt 
tokenizer = AutoTokenizer.from_pretrained(chatglm_path, trust_remote_code=True)
gpt_model = AutoModel.from_pretrained(chatglm_path, trust_remote_code=True, device='cuda')
gpt_model = gpt_model.eval()

def efficientvit(image_path):

    image = Image.open(image_path).convert("RGB")
    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    image= data_transform(image)
    image = torch.unsqueeze(image, dim=0)
    # read class_indices
    json_path = './model/vit/class_indices.json'
    assert os.path.exists(json_path), "file: '{}' does not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # Create a dictionary to map English names to Chinese names
        class_mapping = {
        'Apple_Mosaic': '苹果驳斑病',
        'Apple_Alternaria_Boltch': '苹果斑点落叶病',
        'Apple_Black_rot': '苹果黑腐病',
        'Apple_Brown_Spot': '苹果褐斑病',
        'Apple_Grey_spot': '苹果灰斑病',
        'Apple_healthy': '苹果健康',
        'Apple_Rust': '苹果锈病',
        'Apple_Powdery': '苹果白粉病',
        'Cherry_healthy': '樱桃健康',
        'Cherry_Powdery_Mildew_general': '樱桃白粉病',
        'Citrus_Greening_June_general': '柑橘黄龙病一般',
        'Citrus_Greening_June_serious': '柑橘黄龙病严重',
        'Citrus_healthy': '柑橘健康',
        'Corn_Common_rust': '玉米锈病',
        'Corn_Gray_leaf_spot': '玉米灰斑病',
        'Corn_Northern_Leaf_Blight': '玉米北部叶斑病',
        'Grape mosaic virus': '葡萄花叶病毒',
        'Grape_Leaf_Blight': '葡萄叶斑病',
        'Grape___Esca_(Black_Measles)': '葡萄鹅颈病',
        'Grape_Powdery': '葡萄白粉病',
        'Grape_Black_rot': '葡萄黑腐病',
        'Grape_downy_mildew': '葡萄霜霉病',
        'Grapevine_yellow': '葡萄黄化病',
        'Grape_heathy': '健康葡萄',
        'Orange_Haunglongbing_(Citrus_greening)': '橙子黄龙病',
        'Peach_Bacterial_spot': '桃子细菌性斑点病',
        'Peach_healthy': '桃子健康',
        'Pepper_healthy': '辣椒健康',
        'Pepper_scab_general': '辣椒疮痂病一般',
        'Pepper_bell_Bacterial_spot': '彩椒细菌性斑点病',
        'Pepper_bell_healthy': '彩椒健康',
        'Potato_healthy': '健康马铃薯',
        'Potato_Blight_Fungus': '马铃薯晚疫病真菌',
        'rice_Bacterialblight': '水稻细菌性条斑病',
        'rice_BrownSpot': '水稻褐斑病',
        'rice_Hispa': '水稻蓟马',
        'rice_LeafBlast': '水稻稻瘟病',
        'rice_Tungro': '水稻萎黄病',
        'Soybean_healthy': '大豆健康',
        'Tomato_Bacterial_spot': '番茄细菌斑点病',
        'Tomato_Early_blight': '番茄早疫病',
        'Tomato_healthy': '番茄健康',
        'Tomato_Late_blight': '番茄晚疫病',
        'Tomato_Leaf_Mold': '番茄叶霉病',
        'Tomato_mosaic_virus': '番茄花叶病毒',
        'Tomato_Septoria_leaf_spot': '番茄斑点病',
        'Tomato_Yellow_Leaf_Curl_Virus': '番茄黄化曲叶病毒',
        'Wheal_Leaf_Rust': '小麦叶锈病',
        'Wheat_Healthy': '小麦健康',
        'Strawberry_Leaf_scorch': '草莓叶枯病',
        'strawberry_healthy': '草莓健康',
        'Soybean_healthy': '大豆健康'
        # ... (添加其他类别)
    }
    # prediction
    
    cls_model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(cls_model(image.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()
    print("class: {:10}   prob: {:.3}".format(class_mapping[class_indict[str(predict_cla)]],
                                              predict[predict_cla].numpy()))
    disease=class_mapping[class_indict[str(predict_cla)]]
    #gpt
    # instruction0 ="(1)加强果园管理冬剪后或落叶后彻底清除落叶，集中烧毁，消灭病菌越冬场所。生长季节及时打权、摘心，保持架面通风透光良好，防止果园郁闭，降低环境湿度，创造不利于病害发生的生态条件。\n(2)适当喷药防控灰斑病多为零星发生，—般不需单独进行喷药，结合其他病害防控兼防即可。个别上年病害发生较重的果园，从病害发生初期开始喷药，10-15天1次，连喷2次左右，即可有效控制其发生为害。效果较好的有效药剂有：50％异菌脲可湿性粉剂或45%悬浮剂1000-1500倍液、430克／升戊唑醇悬浮剂3000-4000倍液、10％苯酪甲环唑水分散粒剂1500-2000倍液、70％甲基硫菌灵（甲基托布津）可湿性粉剂或500克／升悬浮剂800-1000倍液、80％代森锰锌（太盛、大生，必得利）可湿性粉剂600~800倍液，30%戊唑．多菌灵（龙灯福连）悬浮剂700-800倍液、41％甲硫．戊唑醇悬浮剂600-700倍液等。"
    # instruction1 ="黑腐病多为零星发生，在搞好果园卫生、清除病残体（将病僵果等病残体清出园外销毁）的基础上，—般不需单独药剂防控。个别受害较重的果园，结合炭疽病的防控进行喷药，即可完全控制该病的发生为害。\n常用有效药剂有：30％戊唑．多菌灵（龙灯福连）悬浮剂800-1000倍液、41%甲硫．戊唑醇悬浮剂600-800倍液、70％甲基硫菌灵（甲基托布津）可湿性粉剂或500克／升悬浮剂800-1000倍液、50％多菌灵可湿性粉剂或500克／升悬浮剂600-800倍液、10％苯酪甲环唑水分散粒剂2000-2500倍液、25％戊唑醇水乳剂2000-2500倍液、430克／升戊唑醇悬浮剂3000-4000倍液、70％丙森锌可湿性粉剂500-600倍液、60％唑酪．代森联水分散粒剂1000-1500倍液等。"
    # instruction2 = "埃斯卡真菌感染的防治方法：埃斯卡真菌给全球范围的葡萄园，尤其是欧洲葡萄园带来负面影响最严重、最普遍的病害之一。葡萄园急救疗法从人类的牙医诊疗手段中得到灵感,采用先进的小型电锯切开葡萄藤主干,把被真菌感染的部分切除取出。这种方法可以保证优质葡萄酒的质量，又避免了拔除病株重新补种的费用，为葡萄酒公司节省资金。葡萄园急救疗法已经为全球知名的伊甘（Chateau d’Yquem）、 拉图（Chateau Latour）、酩悦（Moet&Chandon）等品牌的葡萄园解除了埃斯卡（esca）真菌感染的危害。"
    # instruction3 =""
    # instruction4 ="葡萄黄斑类病毒田间的传播方式不太清楚，可能通过嫁接传播和机械传播，Wah等（1999）发现其可以通过种子传播。葡萄黄斑类病毒通过农具，特别是刀具类(剪枝剪、嫁接刀、镰刀等)容易传染，因此，已污染园地刀具的彻底消毒，以防止其向健壮株的污染则更加重要。用1%福尔马林、1%NaOH、5%NaCl、5%Ca(OCl)2或5%Na3PO4等消毒液浸渍10分钟即可。除福尔马林外，其它4种消毒液均为pHl2以上的强碱。"
    history=[]
    # 更新病害状态
    
    response, history = gpt_model.chat(
        tokenizer,
        f"你现在是作物病害防治助手。请保证使用中文回答问题，我的作物目前状态是：{disease}，我该如何防治？详细描述其中具体的细节,内容不少于八条",
        history
    )
    # 打印模型生成的回答
    print("助手:", response)

    return (f"该叶片状态为{disease}。{response}",history)


def ChatAI(message,his):

    response, history = gpt_model.chat(
        tokenizer,
        message,
        history = his
    )
    
    return response,history


