import json




def get_data(name):
    with open('%s.json' % name, 'r', encoding='utf-8') as json_file:
        return json.loads(json_file.read())

if __name__ == '__main__':
    aim = "人事变动"
    data = get_data(aim)
    print(data)
