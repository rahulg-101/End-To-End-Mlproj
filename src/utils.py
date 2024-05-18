"""
Any functionalities that we are probably writing in a common way
which will be used in entire application
like calling database client, saving model code etc
"""

import os
import sys
import numpy as np
import pandas as pd
import dill

from src.exception import CustomerException


def save_object(filepath,obj):
    try:
        dir_path = os.path.dirname(filepath)

        os.makedirs(dir_path,exist_ok=True)

        with open(filepath,'wb') as f:
            dill.dump(obj,f)

    except Exception as e:
        raise CustomerException(e,sys)