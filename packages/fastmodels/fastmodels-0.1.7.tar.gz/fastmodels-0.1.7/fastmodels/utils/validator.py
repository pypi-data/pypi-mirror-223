import json
from jsonschema import validate, ValidationError


def validate_jsonl(file_path: str):
    """
    验证给定文件路径下的.jsonl文件是否有效。

    这个函数会遍历文件中的每一行，检查每行是否可以解析为一个字典，并且这个字典是否包含 'instruction'，'input' 和 'output' 三个键，每个键的值都是字符串。

    如果遇到任何不符合要求的行，函数会打印出这行内容和一个相关的错误消息，然后返回 False。

    如果所有行都符合要求，函数返回 True。

    Args:
        file_path (str): 要验证的 .jsonl 文件的路径。

    Returns:
        bool: 如果文件符合要求，返回 True；否则返回 False。

    Raises:
        FileNotFoundError: 如果文件路径无效。
        json.JSONDecodeError: 如果行不是有效的 JSON 格式。
    """
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    print(f"Invalid record: {line}")
                    return False
                keys = ['instruction', 'input', 'output']
                if not all(key in data and isinstance(data[key], str) for key in keys):
                    print(f"Invalid record: {line}")
                    return False
            except json.JSONDecodeError:
                print(f"Line is not valid JSON: {line}")
                return False
    return True
