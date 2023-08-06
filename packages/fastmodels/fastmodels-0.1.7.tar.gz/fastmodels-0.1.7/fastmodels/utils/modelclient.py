import requests
import json

def create_completion(prompt: str, modelUuid: str, apiKey: str, n_samples: int=1):
    """
    向指定模型发送文本提示，获取生成的推理结果（Completion）。

    这个函数会向 FastModels API 发送一个 POST 请求，请求内容包含一个文本提示、模型的 UUID、
    授权API KEY、是否使用流式相应、返回结果的数量，然后返回 API 的响应。

    Args:
        prompt (str): 要发送给模型的文本提示。
        modelUuid (str): 要使用的模型的 UUID。
        apiKey (str): 授权的API KEY。
        n_samples (int): 返回结果的数量, 默认为1。

    Returns:
        dict: API 的 JSON 响应，包含生成的完成。

    Raises:
        requests.exceptions.RequestException: 如果请求失败。
    """

    # 当前的Complete接口不支持流式访问
    # TODO: 增加stream_complete接口
    stream = False
    response = requests.post(
        'https://fastmodels.thudbb.com/api/v1/completions',
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {apiKey}'},
        data=json.dumps({'prompt': prompt, 'model_uuid': modelUuid, 'stream': stream, 'n_samples': n_samples})
    )
    return response.json()
