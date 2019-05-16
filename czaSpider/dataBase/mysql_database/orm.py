import logging
import pymysql


def create_mark(num):
    return ', '.join(['?' for _ in range(num)])


def get_mysql_connection():
    global conn
    try:
        conn = pymysql.connect(host='localhost',  # todo, get those data from settings
                               user='root',
                               password='cza19950917',
                               db='scrapy',
                               charset='utf8')
        return True
    except:
        raise Exception('MySQL connect ERROR...')


def select(sql, args=None, size=None):
    global conn
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            res = cur.fetchmany(size)
        else:
            res = cur.fetchall()
        cur.close()
    return res


def execute(sql, args):
    global conn
    with conn.cursor() as cur:
        cur.execute(sql.replace('?', '%s'), args)
        affected = cur.rowcount
        conn.commit()
        cur.close()
    return affected


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return "<%s, %s:%s>" % (self.__class__.__name__, self.column_type, self.name)

    __repr__ = __str__


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(IntegerField, self).__init__(name, "bigint", primary_key, default)


class StringField(Field):
    def __init__(self, name=None, column_type="varchar(100)", primary_key=False, default=None):
        super(StringField, self).__init__(name, column_type, primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super(FloatField, self).__init__(name, "real", primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super(BooleanField, self).__init__(name, "boolean", False, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super(TextField, self).__init__(name, 'text', False, default)


class ModelMetaClass(type):
    def __new__(cls, className, bases, attrs):
        if className == "Model":
            return super(ModelMetaClass, cls).__new__(cls, className, bases, attrs)
        tableName = attrs.get('__table__', None) or className
        new_attrs = attrs.copy()
        mappings = dict()
        fields = []
        primary_key = None
        for key, value in attrs.items():
            if isinstance(value, Field):
                mappings[key] = new_attrs.pop(key)
                if value.primary_key:
                    if primary_key:
                        raise Exception("Duplicate Primary Key!")
                    primary_key = key
                else:
                    fields.append(key)
        if not primary_key:
            raise Exception("You Must Define One Primary Key For: %s" % className)
        polish_field = ', '.join(map(lambda f: '`%s`' % f, fields))
        polish_update_field = ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields))
        new_attrs['__mappings__'] = mappings
        new_attrs['__table__'] = tableName
        new_attrs['__primary_key__'] = primary_key
        new_attrs['__fields__'] = fields
        new_attrs['__select__'] = "SELECT `%s`, %s FROM `%s`" % (primary_key, polish_field, tableName)
        new_attrs['__insert__'] = "INSERT INTO `%s` (%s, `%s`) VALUES (%s)" % (
            tableName, polish_field, primary_key, create_mark(len(mappings)))
        new_attrs['__update__'] = "UPDATE `%s` SET %s WHERE `%s`=?" % (tableName, polish_update_field, primary_key)
        new_attrs['__delete__'] = "DELETE FROM `%s` WHERE `%s`=?" % (tableName, primary_key)
        return super(ModelMetaClass, cls).__new__(cls, className, bases, new_attrs)


class Model(dict, metaclass=ModelMetaClass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self.get(key, None)

    def getValue(self, key):
        return getattr(self, key)

    def getValueOrDefault(self, key):
        value = getattr(self, key)
        if not value:
            default = self.__mappings__[key].default
            if default is not None:
                value = default() if callable(default) else default
                setattr(self, key, value)
        return value

    @classmethod
    def findAll(cls, where=None, args=None, order_by=None, limit=None):
        sql = [cls.__select__]
        if where:
            sql.extend(['where', where])
        if not args:
            args = []
        if order_by:
            sql.extend(['order by', order_by])
        if limit:
            if isinstance(limit, int):
                sql.append('limit ?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('limit ?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid Limit! must be int or tuple')
        res = select(' '.join(sql), args)
        return [cls(**r) for r in res]

    @classmethod
    def findColumn(cls, field, where):
        sql = ['SELECT `%s` _column_ FROM `%s`' % (field, cls.__table__)]
        if where:
            sql.extend(['where', where])
        res = select(' '.join(sql))
        if len(res) == 0:
            logging.warning('Find No Column From SQL!')
            return None
        return res[0]['_column_']

    @classmethod
    def find(cls, primaryKey):
        sql = "%s where `%s`=?" % (cls.__select__, cls.__primary_key__)
        res = select(sql, [primaryKey], 1)
        if len(res) == 0:
            logging.warning('Find no primary key: %s in table' % primaryKey)
            return None
        return cls(**res[0])

    def update_table(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        res = execute(self.__update__, args)
        if res != 1:
            logging.warning('Failed to update by primary key')

    def save(self):
        print(self.__fields__)
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        res = execute(self.__insert__, args)
        if res != 1:
            logging.warning('Failed to insert record')

    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        res = execute(self.__delete__, args)
        if res != 1:
            logging.warning('Failed to remove record!')
