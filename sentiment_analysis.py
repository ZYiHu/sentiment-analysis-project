import os
import json
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# 设置本地模型路径（相对于当前脚本）
MODEL_DIR = os.path.join("models", "sentiment")

# 添加自定义加载函数
def load_model_with_compatibility(model_path):
    """解决PyTorch 2.6+兼容性问题"""
    from transformers import DistilBertForSequenceClassification
    
    # 加载配置
    config = AutoConfig.from_pretrained(model_path)
    
    # 创建空模型
    model = DistilBertForSequenceClassification(config)
    
    # 手动加载权重
    state_dict = torch.load(
        os.path.join(model_path, "pytorch_model.bin"),
        map_location="cpu",
        weights_only=False  # 关键设置
    )
    
    # 加载权重
    model.load_state_dict(state_dict)
    
    return model


def create_compatible_pipeline():
    """创建兼容的Pipeline"""
    from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
    import torch
    
    # 手动加载组件
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_DIR,
        state_dict=torch.load(
            os.path.join(MODEL_DIR, "pytorch_model.bin"),
            map_location="cpu",
            weights_only=False  # 关键设置
        )
    )
    
    # 创建自定义Pipeline
    from transformers import pipeline
    return pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer
    )

def check_model_files():
    """检查所有必需文件是否存在"""
    print("=" * 60)
    print("正在检查模型文件...")
    print("=" * 60)
    
    required_files = [
        ("config.json", "模型配置文件"),
        ("pytorch_model.bin", "模型权重文件"),
        ("vocab.txt", "词汇表文件"),
        ("tokenizer_config.json", "分词器配置文件")
    ]
    
    all_files_present = True
    
    for file_name, description in required_files:
        file_path = os.path.join(MODEL_DIR, file_name)
        exists = os.path.exists(file_path)
        status = "✓ 存在" if exists else "✗ 缺失"
        print(f"{status} | {file_name:25} | {description}")
        
        if not exists:
            all_files_present = False
    
    print("=" * 60)
    
    if all_files_present:
        print("✅ 所有必需文件已就绪！")
        return True
    else:
        print("❌ 缺少必需文件，请下载缺失文件后再运行")
        print(f"下载地址: https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/tree/main")
        return False
    
    json_files = ["config.json", "tokenizer_config.json"]
    for file in json_files:
        path = os.path.join(MODEL_DIR, file)
        try:
            with open(path, 'r') as f:
                json.load(f)
            print(f"✓ JSON格式验证通过: {file}")
        except Exception as e:
            print(f"❌ JSON格式错误: {file} - {str(e)}")
            all_files_present = False

def analyze_with_pipeline():
    """使用Pipeline进行情感分析"""
    print("\n" + "=" * 60)
    print("使用方法1: Transformers Pipeline")
    print("=" * 60)
    
    try:
        # 创建情感分析pipeline
        classifier = pipeline(
            "sentiment-analysis",
            model=MODEL_DIR,  # 直接指定模型目录
            tokenizer=MODEL_DIR  # 直接指定分词器目录
        )
        
        # 分析文本
        texts = [
            "I love using Transformers!",
            "This product is terrible.",
            "The weather is nice today.",
            "I'm frustrated with this issue."
        ]
        
        for text in texts:
            result = classifier(text)
            label = result[0]['label']
            score = result[0]['score']
            
            # 添加表情符号增强可读性
            emoji = "😊" if label == "POSITIVE" else "😞"
            print(f"{emoji} 文本: '{text}'")
            print(f"   情感: {label} (置信度: {score:.4f})")
            print("-" * 50)
            
        print("✅ Pipeline 分析完成！")
        
    except Exception as e:
        print(f"❌ Pipeline 出错: {str(e)}")

def analyze_manually():
    """手动加载模型进行分析"""
    print("\n" + "=" * 60)
    print("使用方法2: 手动加载模型")
    print("=" * 60)
    
    try:
        try:
            import safetensors
            import safetensors.torch
        except ImportError:
            print("安装 safetensors...")
            import subprocess
            subprocess.check_call(["pip", "install", "safetensors"])
            import safetensors
            import safetensors.torch

        # 加载分词器
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        
        # 加载模型
        model = load_safetensors_model(MODEL_DIR)
        
        # 要分析的文本
        text = "Manual loading works perfectly!"
        
        # 预处理文本
        inputs = tokenizer(text, return_tensors="pt")
        
        # 模型推理
        with torch.no_grad():
            outputs = model(**inputs)
        
        # 获取预测结果
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        predicted_class = torch.argmax(probabilities).item()
        sentiment = "POSITIVE" if predicted_class == 1 else "NEGATIVE"
        confidence = probabilities[0][predicted_class].item()
        
        # 添加表情符号
        emoji = "😊" if sentiment == "POSITIVE" else "😞"
        
        print(f"{emoji} 文本: '{text}'")
        print(f"   情感: {sentiment} (置信度: {confidence:.4f})")
        print(f"   原始logits: {logits.tolist()}")
        print(f"   概率分布: {probabilities.tolist()}")
        print("✅ 手动加载分析完成！")
        
    except Exception as e:
        print(f"❌ 手动加载出错: {str(e)}")

# 添加 safetensors 加载函数
def load_safetensors_model(model_path):
    """使用 safetensors 加载模型"""
    from transformers import AutoConfig, DistilBertForSequenceClassification
    import safetensors.torch
    
    # 加载配置
    config = AutoConfig.from_pretrained(model_path)
    
    # 创建空模型
    model = DistilBertForSequenceClassification(config)
    
    # 加载 safetensors 文件
    state_dict = safetensors.torch.load_file(
        os.path.join(model_path, "model.safetensors"),
        device="cpu"
    )
    
    # 加载权重
    model.load_state_dict(state_dict)
    
    return model

if __name__ == "__main__":
    # 检查模型文件
    if check_model_files():
        # 运行两种分析方法
        analyze_with_pipeline()
        analyze_manually()
        
        print("\n🎉 所有分析完成！")
        print("您可以在 models/sentiment/ 目录查看模型文件")
        print("下次运行无需重新下载模型")
    else:
        print("\n请下载缺失文件后重新运行程序")