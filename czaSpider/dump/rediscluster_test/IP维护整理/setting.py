class Setting:
    redis_host = 'localhost'
    redis_port = 6379
    redis_score = 10
    redis_key = 'proxy_ip'
    redis_min_score = 2
    redis_pool_size = 500
    redis_use_pipe = True
    redis_batch_sep = 100

    redis_test_url = 'http://fanyi.youdao.com/'

    allow_status = [200, 302]

    @classmethod
    def get_redis_config(cls):
        return dict(host=cls.redis_host, port=cls.redis_port)


if __name__ == '__main__':
    print(Setting.get_redis_config())
