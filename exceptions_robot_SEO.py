"""
    异常类定义
"""


class ROBOTSEOEXCEPTION(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class NOTUSABLEEXCEPTION(ROBOTSEOEXCEPTION):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
    
    def __str__(self):
        return repr(self.msg)


class INITDRIVEREXCEPTION(ROBOTSEOEXCEPTION):
    def __init__(self, msg):
        super().__init__(msg)
    
    def __str__(self):
        return repr(self.msg)


class GETPAGEERROR(ROBOTSEOEXCEPTION):
    def __init__(self, msg):
        super().__init__(msg)
    
    def __str__(self):
        return repr(self.msg)

