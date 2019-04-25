import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from czaSpider.middlewares.database import user_agent_pool


class baseUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        super(UserAgentMiddleware, self).__init__()
    # def __init__(self, user_agent=''):
    #     self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(user_agent_pool)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    # def test_get_agent(self):
    #     # print(user_agent_pool)
    #     return random.choice(user_agent_pool)


if __name__ == "__main__":
    a = baseUserAgentMiddleware()
    # print(a.test_get_agent())
    # print(a.test_get_agent())
    # print(a.test_get_agent())
    # print(a.test_get_agent())