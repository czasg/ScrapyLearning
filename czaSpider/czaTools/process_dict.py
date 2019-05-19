class Record(dict):
    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value