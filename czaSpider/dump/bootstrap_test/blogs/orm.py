import logging
import aiomysql

logger = logging.getLogger(__name__)

class MySQLer:
    def __init__(self, loop, **kwargs):
        self.init_pool(loop, **kwargs)

    async def init_pool(self, loop, **kwargs):
        self.pool = await aiomysql.create_pool(
            host=kwargs.get('host', 'localhost'),
            port=kwargs.get('port', 3306),
            user=kwargs.get('user', 'root'),
            password=kwargs.get('password', 'cza19950917'),
            db=kwargs.get('db', 'cza'),
            charset=kwargs.get('charset', 'utf8'),
            autocommit=kwargs.get('autocommit', True),
            maxsize=kwargs.get('maxsize', 10),
            minsize=kwargs.get('minsize', 1),
            loop=loop
        )

    async def select(self, sql, args, size=None):
        with (await self.pool) as conn:
            cur = await conn.curosr(aiomysql.DictCursor)
            await cur.execute(sql.replace('?','%s'), args or ())
            res = await cur.fetchmany(size)
