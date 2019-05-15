import pymysql


def create_sql_connection():
    global conn
    conn = pymysql.connect(host='localhost',
                           user='user',
                           password='passwd',
                           db='db',
                           charset='utf8')


def select(sql, args, size):
    global conn
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql, args or ())
        if size:
            res = cur.fetchmany(size)
        else:
            res = cur.fetchall()
        cur.close()
    return res


def execute(sql, args):
    global conn
    with conn.cursor() as cur:
        cur.execute(sql, args)
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
        polish_field = list(map(lambda f: '`%s`' % f, fields))
        new_attrs['__mappings__'] = mappings
        new_attrs['__table__'] = tableName
