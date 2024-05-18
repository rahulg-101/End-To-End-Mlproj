"""
All the model code will be written here from
developing,training to testing, 
no of different kinds of models we need to use,
see scores and confusion matrix here in this file
"""

import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifact','model.pkl')

class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Spliting training and test input data")
            xtrain,ytrain,xtest,ytest = (train_array[:,:-1],
             train_array[:,-1],
             test_array[:,:-1],
             test_array[:,-1]
             )
            
            models = {"Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            model_report:dict=evaluate_models(x=xtrain,y=ytrain,xt=xtest,yt=ytest,
                                             models = models)
            
            ## to get the best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## to get the best model from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info("Best found model on both training and testing dataset")
            
            save_object(
                filepath= self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(xtest)
            r2score = r2_score(ytest,predicted)
            return (r2score,str(best_model))


        except Exception as e:
            raise CustomException(e,sys)
