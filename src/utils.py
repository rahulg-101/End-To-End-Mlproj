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
from sklearn.metrics import r2_score

from src.exception import CustomException


def save_object(filepath,obj):
    try:
        dir_path = os.path.dirname(filepath)

        os.makedirs(dir_path,exist_ok=True)

        with open(filepath,'wb') as f:
            dill.dump(obj,f)

    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_models(x,y,xt,yt,models):
    try:
        report ={}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            model.fit(x,y)
            ytrain_pred  = model.predict(x)
            ytest_pred  = model.predict(xt)

            train_model_score = r2_score(y,ytrain_pred)

            test_model_score = r2_score(yt,ytest_pred)

            report[list(models.keys())[i]] = test_model_score

            return report
        
    except Exception as e:
        raise CustomException(e,sys)