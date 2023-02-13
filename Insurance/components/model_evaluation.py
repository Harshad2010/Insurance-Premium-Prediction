from Insurance.predictor import ModelResolver
from Insurance.entity import config_entity, artifacts_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from sklearn.metrics import r2_score
import pandas as pd
import sys
import os
from Insurance.config import TARGET_COLUMN



class ModelEvaluation():
    
    def __init__(self,
        model_eval_config: config_entity.ModelEvaluationConfig,
        data_ingestion_artifact : artifacts_entity.DataIngestionArtifact,
        data_tranformation_artifact : artifacts_entity.DataTransformationArtifact,
        model_trainer_artifact : artifacts_entity.ModelTrainerArtifact
        ):
        
        try:
            logging.info(f"{'>>'*20} MODEL EVALUATION {'<<'*20} ")
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_tranformation_artifact = data_tranformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InsuranceException(e,sys)
        
    def initiate_model_evaluation(self)-> artifacts_entity.ModelEvaluationArtifact :
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            
            if latest_dir_path == None:
                model_eval_artifact = artifacts_entity.ModelEvaluationArtifact(is_model_accepted= True, improved_accuracy= None)
                
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                
                return model_eval_artifact

            
        except Exception as e:
            raise InsuranceException(e,sys)
        
        

