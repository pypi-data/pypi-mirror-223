import os
import argparse
from fastmodels.utils.validator import validate_jsonl
from fastmodels.utils.modelclient import create_completion


def main():
    parser = argparse.ArgumentParser(description='Validate a JSONL file.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a parser for the "validate_data" command
    parser_validate = subparsers.add_parser('validate_data', help='Validate a JSONL file.')
    parser_validate.add_argument('-f', '--file', type=str, required=True,
                                 help='The path to the JSONL file to validate.')

    # Create a parser for the "complete" command
    parser_complete = subparsers.add_parser('complete', help='Complete the prompt using a specific model.')
    parser_complete.add_argument('-m', '--modelUuid', type=str, required=True, help='The UUID of the model to use.')
    parser_complete.add_argument('-p', '--prompt', type=str, required=True, help='The prompt to complete.')
    # 当前的Complete接口不支持流式访问
    # TODO: 增加stream_complete接口
    # parser_complete.add_argument('-s', '--stream', type=bool, required=False, default=True, help='Whether to use streaming response.')
    parser_complete.add_argument('-n', '--n_samples', type=int, required=False, default=1, help='Number of results returned')

    args = parser.parse_args()
    if args.command == 'validate_data':
        is_valid = validate_jsonl(args.file)
        if is_valid:
            print('The JSONL file is valid.')
            print('您的数据文件是有效的。')
        else:
            print('The JSONL file is invalid. Please make sure each line conforms to the format:')
            print('{"instruction": "<text>", "input": "<text>", "output":"<text>"}')
            print('您的数据文件存在问题。')
    elif args.command == 'complete':
        api_key = os.getenv('FASTMODELS_API_KEY')
        if api_key is None:
            raise ValueError("请先设置API key FASTMODELS_API_KEY")
        response_json = create_completion(args.prompt, args.modelUuid, api_key, args.n_samples)
        print(response_json)


if __name__ == '__main__':
    main()
