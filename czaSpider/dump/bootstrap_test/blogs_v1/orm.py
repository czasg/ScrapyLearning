import logging
import aiomysql

from tools.man_error import *

logger = logging.getLogger(__name__)


def get_args(num):
    return ', '.join(['?' for _ in range(num)])


async def init_pool(loop, **kwargs):
    global pool
    pool = await aiomysql.create_pool(
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


async def select(sql, args, size=None):
    global pool
    with (await pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        res = await cur.fetchmany(size) if size else await cur.fetchall()
        await cur.close()
        logger.info('return %d from MySQL-DB' % len(res))
        return res


async def execute(sql, args):
    with (await pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            res = cur.rowcount
            await cur.close()
        except:
            import traceback
            print(sql.replace('?', '%s'), args)
            print(traceback.format_exc())
            raise MySQLExecuteError('500', 'execute sql "%s" error' % sql)
    return res


class Field:
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return "<%s, %s: %s>" % (self.__class__.__name__, self.column_type, self.name)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(IntegerField, self).__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super(FloatField, self).__init__(name, 'read', primary_key, default)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super(StringField, self).__init__(name, ddl, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super(BooleanField, self).__init__(name, 'boolean', False, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super(TextField, self).__init__(name, 'text', False, default)


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', name)
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings.setdefault(k, v)
                if v.primary_key:
                    if primaryKey:
                        raise PrimaryKeyDuplicated('500', 'primary key is duplicated')
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise PrimaryKeyUndefined('500', 'primary key is not defined')
        for k in mappings.keys():
            attrs.pop(k)
        secFields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(secFields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            tableName, ', '.join(secFields), primaryKey, get_args(len(mappings)))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__remove__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaClass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('"Model" object has no attribute "%s"' % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if not value:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, orderBy=None, limit=None):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        if args is None:
            args = []
        if limit:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        res = await select(' '.join(sql), args)
        return [cls(**r) for r in res]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        res = await select(' '.join(sql), args, 1)
        return None if len(res) == 0 else res[0]['_num_']

    @classmethod
    async def find(cls, pk):
        sql = '%s where `%s`=?' % (cls.__select__, cls.__primary_key__)
        res = await select(sql, [pk], 1)
        return None if len(res) == 0 else cls(**res[0])

    async def update_table(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        await execute(self.__update__, args)

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        await execute(self.__insert__, args)

    async def remove(self, id=None):
        args = [id or self.getValue(self.__primary_key__)]
        await execute(self.__remove__, args)
