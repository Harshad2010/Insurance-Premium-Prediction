from Insurance.entity import config_entity, artifacts_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from typing import Optional
import sys
import os
from sklearn.pipeline import Pipeline
import pandas as pd
from Insurance import utils
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

class ModelTrainer:

    def __init__(self,
                 model_trainer_config: config_entity.ModelTrainerConfig,
                 data_transformation_artifact :artifacts_entity.DataTransformationArtifact):
        try:
            logging.info(f" {'>>'*20} MODEL TRAINER {'<<'*20} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            raise InsuranceException(e,sys)
            
    def train_model(self,x,y):
        try:
            lr = LinearRegression()
            lr.fit(x,y)
            return lr
        except Exception as e:
            raise InsuranceException(e,sys)
        
    def initiate_model_trainer(self,)-> artifacts_entity.ModelTrainerArtifact :
        try:
            logging.info(f"Loading train and test array.")
            train_file_path = self.data_transformation_artifact.transformed_train_path
            test_file_path = self.data_transformation_artifact.transformed_test_path
            
            #train_arr = utils.load_numpy_array_data(file_path=train_file_path )
            #test_arr = utils.load_numpy_array_data(file_path=test_file_path)
            
            train_arr = np.load(train_file_path)
            test_arr = np.load(test_file_path)
            
            
            #train_arr = np.array(train_arr)
            #test_arr = np.array(test_arr)
            print(train_arr)
            print(test_arr)
            
            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            
            logging.info(f"Train the model")
            model = self.train_model(x=x_train, y=y_train)
            
            logging.info(f"Calculating r2 train score")
            y_hat_train = model.predict(x_train)
            r2_train_score = r2_score(y_true=y_train, y_pred=y_hat_train)
            
            logging.info(f"Calculating r2 test score")
            y_hat_test = model.predict(x_test)
            r2_test_score = r2_score(y_true=y_test, y_pred=y_hat_test)
            
            logging.info(f"train score:{r2_train_score} and tests score {r2_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if r2_test_score < self.model_trainer_config.expected_score :
                raise Exception(f" Model is not as good as it's score is less than expected score : {self.model_trainer_config.expected_score}, actual score : {r2_test_score}")
            
            logging.info(f"Checking if our model is overfiiting or not")    
            diff = abs(r2_train_score - r2_test_score)
            
            if diff > self.model_trainer_config.overfitting_threshold :
                raise Exception(f" Model is overfitting,  train/test score diff : {diff} is more than overfitting threshold :{self.model_trainer_config.overfitting_threshold }")
            
            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj= model)
            
            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact = artifacts_entity.ModelTrainerArtifact(
                                    model_path =  self.model_trainer_config.model_path,
                                    r2_train_score = r2_train_score,
                                    r2_test_score = r2_test_score
                                    )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
            raise InsuranceException(e,sys)
                
                
            
            

        
    