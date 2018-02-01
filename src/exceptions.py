# Copyright 2017 SuperDARN Canada
#
# Marina Schmidt
#
# exception.py
# 2018-01-26

class RSTException(Exception):

    def __init__(self,function_name,return_value):
        self.function_name = function_name
        self.return_value = return_value
        self.message = "RST function {} failed with"
        " error value of {} ".format(function_name,return_value)
        Exception.__init__(self,self.message)


