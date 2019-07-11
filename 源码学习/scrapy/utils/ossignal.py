
from __future__ import absolute_import
import signal

from twisted.internet import reactor


signal_names = {} # {<Signals.SIGABRT: 22>: 'SIGABRT', <Signals.SIGBREAK: 21>: 'SIGBREAK', <Signals.SIGFPE: 8>: 'SIGFPE', <Signals.SIGILL: 4>: 'SIGILL', <Signals.SIGINT: 2>: 'SIGINT', <Signals.SIGSEGV: 11>: 'SIGSEGV', <Signals.SIGTERM: 15>: 'SIGTERM'}
for signame in dir(signal):
    if signame.startswith('SIG') and not signame.startswith('SIG_'):
        signum = getattr(signal, signame)
        if isinstance(signum, int):
            signal_names[signum] = signame


def install_shutdown_handlers(function, override_sigint=True):
    """Install the given function as a signal handler for all common shutdown
    signals (such as SIGINT, SIGTERM, etc). If override_sigint is ``False`` the
    SIGINT handler won't be install if there is already a handler in place
    (e.g.  Pdb)
    """
    reactor._handleSignals()
    signal.signal(signal.SIGTERM, function)  # 这个是关闭程序的信号
    if signal.getsignal(signal.SIGINT) == signal.default_int_handler or \
            override_sigint:
        signal.signal(signal.SIGINT, function)  # 这个是接收ctrl+c信号的
    # Catch Ctrl-Break in windows
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, function)


# signal.signal(signal.SIGTERM, self._term_handler)   # SIGTERM 关闭程序信号
# signal.signal(signal.SIGINT, self._term_handler)  # 接收ctrl+c 信号
"""
SIGINT    终止进程     中断进程  (control+c)
SIGTERM   终止进程     软件终止信号
SIGKILL   终止进程     杀死进程
SIGALRM   闹钟信号

1(被动式)  内核检测到一个系统事件.例如子进程退出会像父进程发送SIGCHLD信号.键盘按下control+c会发送SIGINT信号
2(主动式)  通过系统调用kill来向指定进程发送信号
"""