"""
Exception handling code will be written here
"""
from src.logger import logging
import sys  
"""
The sys module in Python provides various functions and variables that 
are used to manipulate different parts of the Python
runtime environment. It allows operating on the interpreter as
it provides access to the variables and functions that
 interact strongly with the interpreter. 
"""


def error_msg_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_msg = f"Error occured in python script name {file_name} at line number {line_number} & the error message is {str(error)}"
    return error_msg

class CustomerException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_msg_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    try :
        a = 1/0
    except Exception as e:
        logging.info("Divide by Zero Error")
        raise CustomerException(e,sys)