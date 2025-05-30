import os
import requests
from pathlib import Path

MODEL_DIR = Path("models/sentiment")
MODEL_URLS = {
    "config.json": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/config.json",
    "pytorch_model.bin": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/pytorch_model.bin",
    "vocab.txt": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/vocab.txt",
    "tokenizer_config.json": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/tokenizer_config.json"
}

def download_model():
    print("准备下载情感分析模型文件...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    for filename, url in MODEL_URLS.items():
        file_path = MODEL_DIR / filename
        
        if file_path.exists():
            print(f"✓ 已存在: {filename}")
            continue
            
        print(f"下载: {filename}...")
        try:
            # 处理二进制文件
            if filename.endswith(".bin"):
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            # 处理文本文件
            else:
                response = requests.get(url)
                response.encoding = "utf-8"
                response.raise_for_status()
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                    
            print(f"✓ 下载完成: {filename}")
        except Exception as e:
            print(f"✗ 下载失败: {filename} - {str(e)}")
    
    print("\n模型文件准备就绪！现在可以运行程序了。")

if __name__ == "__main__":
    download_model()