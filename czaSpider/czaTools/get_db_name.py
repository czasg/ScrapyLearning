import time


def get_collection_name(name, timeStr=False):
    name = name.replace("-","_") + "Coll"
    if timeStr:
        timeStr = time.strftime("%Y%m%d", time.localtime())
        return name + timeStr
    return name

def get_database_name(name, timeStr=False):
    # name = name.replace("-","_") + "Db"
    # if timeStr:
    #     timeStr = time.strftime("%Y%m%d", time.localtime())
    #     return name + timeStr
    return name[name.rfind('-') + 1:]


if __name__ == "__main__":
    name = "ziru-housePrice"
    print(get_collection_name(name, timeStr=True))
    print(get_database_name(name))