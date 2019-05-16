import time
import uuid

from czaSpider.dataBase.mysql_database.orm import *


def next_id():
    return "%015d%s000" % (int(time.time() * 1000), uuid.uuid4().hex)


class housePriceDB(Model):
    __table__ = "housePrice"

    id = StringField(column_type="varchar(50)", primary_key=True, default=next_id)
    house_price = FloatField()
    house_place = StringField(column_type="varchar(100)")
    house_name = StringField(column_type="varchar(50)")
    house_area = StringField(column_type="varchar(50)")
    house_floor = StringField(column_type="varchar(50)")
    house_scale = StringField(column_type="varchar(50)")
    distance_from_subway = StringField(column_type="varchar(50)")
    created_at = FloatField(default=time.time)
