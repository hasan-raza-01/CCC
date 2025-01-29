import sys
from package.logger import logging

def get_mssg(mssg, sys_obj):
    _, _, exc_traceback = sys_obj.exc_info()
    file_path = exc_traceback.tb_frame.f_code.co_filename
    line_no = exc_traceback.tb_lineno
    detail_mssg = f"Error occured !!!! \n\n\t- file: {file_path} \n\t- line: {line_no} \n\t- message: {mssg}"

    return detail_mssg


class CustomException(Exception):
    def __init__(self, mssg, sys_obj):
        super().__init__(mssg)
        self.mssg = get_mssg(mssg, sys_obj)

    def __str__(self) -> str:
        return self.mssg


if __name__=="__main__":
    try:
        1/0
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
