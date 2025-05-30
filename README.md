# sentiment-analysis-project
My first NLP project for sentiment analysis using Hugging Face Transformers.


# 情感分析 NLP 项目

这是我的第一个 NLP 项目，使用 Hugging Face Transformers 实现本地情感分析。

## 项目功能
- 使用预训练的 DistilBERT 模型
- 支持两种分析方式：
  - Pipeline API（简单快捷）
  - 手动加载模型（灵活可控）
- 可分析任意英文文本的情感倾向

## 运行效果截图
![情感分析结果](screenshot.png)  <!-- 如果上传了截图 -->

## 如何运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/你的用户名/你的仓库名.git
   cd 你的仓库名
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 下载模型文件：
   - [config.json](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/config.json)
   - [pytorch_model.bin](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/pytorch_model.bin)
   - [vocab.txt](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/vocab.txt)
   - [tokenizer_config.json](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/raw/main/tokenizer_config.json)
   
   将上述文件放入 `models/sentiment/` 目录

4. 运行主程序：
   ```bash
   python sentiment_analysis.py
   ```

## 项目结构
```
项目目录结构...
```

## 学习收获
在这个项目中，我学会了：
- 使用 Hugging Face Transformers 库
- 加载预训练模型
- 处理文本数据
- 进行情感分析
- 解决环境配置问题
- 使用Git管理代码

## 未来改进计划
- [ ] 添加交互式界面
- [ ] 支持更多语言
- [ ] 添加模型微调功能
- [ ] 部署为Web应用