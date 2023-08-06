# FastModels Command-line Interface and Python Library

一个python library，方便用户进行数据预处理、和通过API访问FastModels服务。

### Installation

要安装FastModels Python库，请运行以下命令：
```
pip install fastmodels
```

### Data Validation

您可以使用FastModels Python库验证您的JSONL数据文件。数据文件应遵循以下格式：每行为: 
`{"instruction": "<text>", "input": "<text>", "output": "<text>"}` .

要验证数据文件，请使用以下命令：
```
fastmodels validate_data -f your_data_file.jsonl
```

### Setting API Key

在通过API访问FastModels服务之前，您需要将API密钥设置为环境变量。将`your_api_key`替换为您的实际API密钥。

```
export FASTMODELS_API_KEY=your_api_key
```

### Inference Completion

您可以使用FastModels的特定模型来完成推理。将`MODEL_UUID`替换为您要使用的模型的UUID，并将`PROMPT`替换为您的实际提示。

```
fastmodels complete -m "MODEL_UUID" -p "PROMPT"
```

## Python Library Usage

您还可以直接在Python代码中使用FastModels Python库。以下是使用示例：

```python
import fastmodels

# Set the API key
fastmodels.set_apikey("your_api_key")

# Inference using the specified model and prompt
response = fastmodels.complete("Your prompt", "Your model_uuid")

print(response)
```

## Development and Uploading to PyPI
To test the library locally, run `pip install -e .` in the fastmodels directory.

### Uploading to PyPl:
1. 安装必要的包`pip install setuptools wheel twine`
2. 打包`python setup.py sdist bdist_wheel`
3. 测试上传（可选）`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
4. 实际上传`twine upload dist/*`



