from socket import *
import threading, sys, json, re

HOST = '127.0.0.1'  ##
PORT = 8022
BUFSIZE = 1024  ##缓冲区大小  1K
ADDR = (HOST, PORT)
myre = r"^[_a-zA-Z]\w{0,}"
tcpCliSock = socket(AF_INET, SOCK_STREAM)
userAccount = None


def register():
    print("""
    Glad to have you a member of us!
    """)
    accout = input('Please input your account: ')
    if not re.findall(myre, accout):
        print('Account illegal!')
        return None
    password1 = input('Please input your password: ')
    password2 = input('Please confirm your password: ')
    if not (password1 and password1 == password2):
        print('Password not illegal!')
        return None
    global userAccount
    userAccount = accout
    regInfo = [accout, password1, 'register']
    datastr = json.dumps(regInfo)
    tcpCliSock.send(datastr.encode('utf-8'))  # 传入的也是一个list
    data = tcpCliSock.recv(BUFSIZE)
    data = data.decode('utf-8')  # 返回的是一个标记
    if data == '0':
        print('Success to register!')
        return True
    elif data == '1':
        print('Failed to register, account existed!')
        return False
    else:
        print('Failed for exceptions!')
        return False


def login():
    print("""
    Welcome to login in!
    """)
    accout = input('Account: ')
    if not re.findall(myre, accout):
        print('Account illegal!')
        return None
    password = input('Password: ')
    if not password:
        print('Password illegal!')
        return None
    global userAccount
    userAccount = accout
    loginInfo = [accout, password, 'login']
    datastr = json.dumps(loginInfo)
    tcpCliSock.send(datastr.encode('utf-8'))  # 哦，传过去的居然是一个list哦，这倒是让我吃惊
    data = tcpCliSock.recv(BUFSIZE)  # send和recv两个方法
    if data == '0':
        print('Success to login!')
        return True
    else:
        print('Failed to login in(user not exist or username not match the password)!')
        return False


def addGroup():
    groupname = input('Please input group name: ')
    if not re.findall(myre, groupname):
        print('group name illegal!')
        return None
    return groupname


def chat(target):  # 这玩意还是通过socket连接进行的啊
    while True:
        print('{} -> {}: '.format(userAccount, target))
        msg = input()
        if len(msg) > 0 and not msg in 'qQ':
            if 'group' in target:
                optype = 'cg'
            else:
                optype = 'cp'

            dataObj = {'type': optype, 'to': target, 'msg': msg, 'froms': userAccount}
            datastr = json.dumps(dataObj)
            tcpCliSock.send(datastr.encode('utf-8'))
            continue
        elif msg in 'qQ':
            break
        else:
            print('Send data illegal!')


class inputdata(threading.Thread):
    def run(self):
        menu = """
                        (CP): Chat with individual
                        (CG): Chat with group member
                        (AG): Add a group
                        (EG): Enter a group
                        (H):  For help menu
                        (Q):  Quit the system
                        """
        print(menu)
        while True:
            operation = input('Please input your operation("h" for help): ')
            if operation in 'cPCPCpcp':
                target = input('Who would you like to chat with: ')
                chat(target)  # 当你需要直接连接，建立一个chat连接
                continue
            if operation in 'cgCGCgcG':
                target = input('Which group would you like to chat with: ')
                chat('group' + target)  # 仍然是一个chat连接
                continue
            if operation in 'agAGAgaG':
                groupName = addGroup()  # 创建一个组连接
                if groupName:
                    dataObj = {'type': 'ag', 'groupName': groupName}
                    dataObj = json.dumps(dataObj)
                    tcpCliSock.send(dataObj.encode('utf-8'))  # 通过socket连接发送一个dict字典
                continue
            if operation in 'egEGEgeG':
                groupname = input('Please input group name fro entering: ')
                if not re.findall(myre, groupname):
                    print('group name illegal!')
                    return None
                dataObj = {'type': 'eg', 'groupName': 'group' + groupname}
                dataObj = json.dumps(dataObj)
                tcpCliSock.send(dataObj.encode('utf-8'))
                continue
            if operation in 'hH':
                print(menu)
                continue

            if operation in 'qQ':
                sys.exit(1)
            else:
                print('No such operation!')


class getdata(threading.Thread):
    def run(self):
        while True:
            data = tcpCliSock.recv(BUFSIZE).decode('utf-8')  # 这里的数据是后台返回过来的
            if data == '-1':  # -1 就是没有找到目标咯
                print('can not connect to target!')
                continue
            if data == 'ag0':
                print('Group added!')
                continue
            if data == 'eg0':
                print('Entered group!')
                continue
            if data == 'eg1':
                print('Failed to enter group!')
                continue

            dataObj = json.loads(data)  # 后台传过来的数据是dict
            if dataObj['type'] == 'cg':  # 看type，只有是cg才是对的呀
                print('{}(from {})-> : {}'.format(dataObj['froms'], dataObj['to'], dataObj['msg']))
            else:
                print('{} ->{} : {}'.format(dataObj['froms'], userAccount, dataObj['msg']))


def main():
    try:
        tcpCliSock.connect(ADDR)  # 这里是一个socket连接
        print('Connected with server')
        while True:
            loginorReg = input('(l)ogin or (r)egister a new account: ')
            if loginorReg in 'lL':
                log = login()
                if log:
                    break
            if loginorReg in 'rR':
                reg = register()
                if reg:
                    break

        myinputd = inputdata()
        mygetdata = getdata()
        myinputd.start()  # threading.Thread这是开了一个线程的意思嘛
        mygetdata.start()
        myinputd.join()
        mygetdata.join()

    except Exception:
        print('error')
        tcpCliSock.close()
        sys.exit()


if __name__ == '__main__':
    main()
