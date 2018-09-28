import json


def load(format, input, output):
    for item in format.split(','):
        if '|' in item:
            pair = item.split('|')
            output[pair[1]] = input[pair[0]] if pair[0] in input else None
        else:
            output['meta'][item] = input[item] if item in input else ''
    return output


def explain(format, input, output):
    for item in format.split(','):
        if '|' in item:
            pair = item.split('|')
            output[pair[0]] = input[pair[1]] if pair[1] in input else None
    if 'meta' in input and input['meta']:
        meta = json.loads(input['meta'])
        for key in meta:
            output[key] = meta[key]
    return output