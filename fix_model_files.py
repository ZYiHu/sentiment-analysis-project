import os
import json
import requests

MODEL_DIR = os.path.join("models", "sentiment")
MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

def fix_config_file():
    """修复或重新下载 config.json 文件"""
    config_path = os.path.join(MODEL_DIR, "config.json")
    
    # 尝试读取现有文件
    try:
        with open(config_path, 'r') as f:
            json.load(f)  # 尝试解析JSON
        print("✅ config.json 文件格式正确")
        return True
    except:
        print("⚠️ 检测到 config.json 文件格式错误，尝试修复...")
    
    # 尝试从网络下载正确的配置文件
    try:
        url = f"https://huggingface.co/{MODEL_NAME}/raw/main/config.json"
        response = requests.get(url)
        response.raise_for_status()
        
        with open(config_path, 'w') as f:
            f.write(response.text)
        
        # 验证修复
        with open(config_path, 'r') as f:
            json.load(f)
        print("✅ config.json 文件已成功修复")
        return True
    except Exception as e:
        print(f"❌ 修复失败: {str(e)}")
        return False

def check_all_files():
    """检查所有必需文件"""
    required_files = {
        "config.json": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/config.json",
        "pytorch_model.bin": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/pytorch_model.bin",
        "vocab.txt": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/vocab.txt",
        "tokenizer_config.json": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/tokenizer_config.json"
    }
    
    print("=" * 60)
    print("模型文件完整性检查")
    print("=" * 60)
    
    all_ok = True
    
    for file, url in required_files.items():
        path = os.path.join(MODEL_DIR, file)
        exists = os.path.exists(path)
        status = "✓ 存在" if exists else "✗ 缺失"
        
        # 检查文件大小
        size_info = ""
        if exists:
            size = os.path.getsize(path)
            size_info = f"大小: {size/1024:.1f} KB" if size < 1024*1024 else f"大小: {size/(1024*1024):.1f} MB"
        
        print(f"{status} | {file:25} | {size_info}")
        
        if not exists:
            all_ok = False
            print(f"   下载链接: {url}")
    
    print("=" * 60)
    return all_ok

if __name__ == "__main__":
    # 确保目录存在
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # 检查并修复配置文件
    if fix_config_file():
        print("\n配置文件修复成功！")
    
    # 检查其他文件
    if not check_all_files():
        print("\n⚠️ 部分文件缺失，请从提供的链接下载")
    
    print("\n修复完成！请重新运行 sentiment_analysis.py")