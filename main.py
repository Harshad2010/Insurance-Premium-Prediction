from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os
import sys
#from Insurance.utils import get_collection_as_dataframe
from data_dump import DATABASE_NAME, COLLECTION_NAME
from Insurance.entity import config_entity
from Insurance.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataValidationConfig
from Insurance.components.data_ingestion import DataIngestion
from Insurance.entity.artifacts_entity import DataIngestionArtifact
from Insurance.components.data_validation import DataValidation
from Insurance.entity.artifacts_entity import DataValidationArtifact
from Insurance.components.data_transformation import Data_Transformation
#def test_logger_and_exception():
    #try:
        
        #logging.info("Starting the test_logger_and_exception")
        #result =3/0
        #print(result)
        #logging.info('Ending point of test_logger_and_exception')
    
    #except Exception as e :
        
        #logging.debug(str(e))
        #raise InsuranceException(e,sys)
    
if __name__ == '__main__':
    
    try:
        #start_training_pipeline()
        #test_logger_and_exception()
        #get_collection_as_dataframe(database_name= DATABASE_NAME , collection_name = COLLECTION_NAME)
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        # Data Validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config = training_pipeline_config)
        data_validation = DataValidation(data_validation_config= data_validation_config,
                                            data_ingestion_artifact= data_ingestion_artifact)   
        data_validation_artifact = data_validation.initiate_data_validation()
        
        # Data tranformation
        data_tranformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_tranformation = Data_Transformation(data_transformation_config=data_tranformation_config, 
                                                 data_ingestion_artifact= data_ingestion_artifact)
        data_transformation_artifact = data_tranformation.initiate_data_transformation()
        
    except Exception as e:
        print(e)