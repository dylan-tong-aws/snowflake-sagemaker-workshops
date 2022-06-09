#!/usr/bin/env python

import time
import uuid
import sagemaker
import os
import json
import boto3

import utils.dw

from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.dataset_definition.inputs import AthenaDatasetDefinition, DatasetDefinition, RedshiftDatasetDefinition
from sagemaker.processing import Processor
from sagemaker.network import NetworkConfig
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.inputs import TransformInput
from sagemaker.workflow.steps import TransformStep
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
)
from sagemaker.workflow.pipeline import Pipeline

__author__ = "Dylan Tong"
__credits__ = ["Dylan Tong"]
__license__ = "Apache"
__version__ = "0.1"
__maintainer__ = "Dylan Tong"
__email__ = "dylatong@amazon.com"
__status__ = "Prototype"

class BlueprintFactory() :

    def __init__(self, config):
        
        self.dw_output_name = config["dw_output_name"] if "dw_output_name" in config else None        
        if not self.dw_output_name :
            raise Exception("Missing configuration for dw_output_name.")
        
        self.dw_instance_count           = config["dw_instance_count"] if "dw_instance_count" in config else 1
        self.dw_instance_type            = config["dw_instance_type"] if "dw_instance_type" in config else "ml.m5.4xlarge"
        self.dw_volume_size_in_gb        = config["dw_volume_size_in_gb"] if "dw_volume_size_in_gb" in config else 30
        self.dw_output_content_type      = config["dw_output_content_type"] if "dw_output_content_type" in config else "CSV"
        self.dw_enable_network_isolation = config["dw_enable_network_isolation"] if "dw_enable_network_isolation" in config else False
        
        self.dw_flow_filepath            = config["dw_flow_filepath"] if "dw_flow_filepath" in config else ""
        self.dw_flow_filename            = config["dw_flow_filename"] if "dw_flow_filename" in config else None
        if not self.dw_flow_filename :
            raise Exception("Missing configuration for dw_flow_filename")
            
        self.dw_source_bucket            = config["dw_source_bucket"] if "dw_source_bucket" in config else None
        if not self.dw_source_bucket :
            raise Exception("Missing configuration for dw_source_bucket")
                 
        self.batch_instance_count        = config["batch_instance_count"] if "batch_instance_count" in config else 1
        self.batch_instance_type         = config["batch_instance_type"] if "batch_instance_type" in config else "ml.c5.2xlarge"   
        self.batch_s3_output_uri         = config["batch_s3_output_uri"] if "batch_s3_output_uri" in config else None
    
        if not self.batch_s3_output_uri :
            raise Exception("Missing configuration for batch_s3_output_uri")
        
        self.batch_in_filter             = config["batch_in_filter"] if "batch_in_filter" in config else "$"
        self.batch_join_source           = config["batch_join_source"] if "batch_join_source" in config else "None"
        self.batch_out_filter            = config["batch_out_filter"] if "batch_out_filter" in config else "$"
        self.batch_split_type            = config["batch_split_type"] if "batch_split_type" in config else "None"
            
        self.batch_instance_count        = config["batch_instance_count"] if "batch_instance_count" in config else 1
        self.batch_instance_type         = config["batch_instance_type"] if "batch_instance_type" in config else "ml.c5.2xlarge" 
        
        self.sm_estimator                = config["sm_estimator"] if "sm_estimator" in config else None
        if not self.sm_estimator :
            raise Exception("Missing configuration for sm_estimator")
     
        self.wf_instance_count           = config["wf_instance_count"] if "wf_instance_count" in config else 1
        self.wf_instance_type            = config["wf_instance_type"] if "wf_instance_type" in config else "ml.m5.4xlarge"       
        
    def get_batch_pipeline(self) :    
                
        iam_role = sagemaker.get_execution_role()
        region   = boto3.session.Session().region_name

        data_sources = []
        sess = sagemaker.Session()
        flow_export_id = f"{time.strftime('%d-%H-%M-%S', time.gmtime())}-{str(uuid.uuid4())[:8]}"
        flow_export_name = f"flow-{flow_export_id}"
        s3_output_prefix = f"export-{flow_export_name}/output"
        s3_output_path = f"s3://{self.dw_source_bucket}/{s3_output_prefix}"

        processing_job_output = ProcessingOutput(
            output_name=self.dw_output_name,
            source="/opt/ml/processing/output",
            destination=s3_output_path,
            s3_upload_mode="EndOfJob"
        )

        with open(os.path.join(self.dw_flow_filepath, self.dw_flow_filename)) as f:
            flow = json.load(f)

        s3_client = boto3.client("s3")
        s3_client.upload_file(self.dw_flow_filename, self.dw_source_bucket, f"data_wrangler_flows/{flow_export_name}.flow")
        flow_s3_uri = f"s3://{self.dw_source_bucket}/data_wrangler_flows/{flow_export_name}.flow"

        flow_input = ProcessingInput(
            source=flow_s3_uri,
            destination="/opt/ml/processing/flow",
            input_name="flow",
            s3_data_type="S3Prefix",
            s3_input_mode="File",
            s3_data_distribution_type="FullyReplicated"
        )

        processing_job_name = f"data-wrangler-flow-processing-{flow_export_id}"
        
        ## This script was exported for version 1.5.3. As it currently stands, there's no generic script
        ## if this script stops working, you need to export the flow and refactor the code.
        container_uri        = utils.dw.get_data_wrangler_container_uri(region, "1.x")
        container_uri_pinned = utils.dw.get_data_wrangler_container_uri(region, "1.5.3")
        output_config = {
            self.dw_output_name: {
                "content_type": self.dw_output_content_type
            }
        }

        processor = Processor(
            role=iam_role,
            image_uri=container_uri,
            instance_count=self.dw_instance_count,
            instance_type=self.dw_instance_type,
            volume_size_in_gb=self.dw_volume_size_in_gb,
            network_config=NetworkConfig(enable_network_isolation=self.dw_enable_network_isolation),
            sagemaker_session=sess
        )

        data_wrangler_step = ProcessingStep(
            name="DataWranglerProcessingStep",
            processor=processor,
            inputs=[flow_input] + data_sources, 
            outputs=[processing_job_output],
            job_arguments=[f"--output-config '{json.dumps(output_config)}'"],
        )

        transformer = self.sm_estimator.transformer(instance_count = self.batch_instance_count,
                                                    strategy       ='SingleRecord',
                                                    assemble_with  ='Line',
                                                    instance_type  = self.batch_instance_type,
                                                    accept         = 'text/csv',
                                                    output_path    = self.batch_s3_output_uri)

        transform_step = TransformStep(name="DefaultRiskScores",
                                       transformer=transformer,
                                       inputs=TransformInput(  input_filter=self.batch_in_filter,
                                                               output_filter=self.batch_out_filter,
                                                               join_source=self.batch_join_source,
                                                               split_type=self.batch_split_type,
                                                               data=data_wrangler_step
                                                              .properties
                                                              .ProcessingOutputConfig
                                                              .Outputs[self.dw_output_name].S3Output.S3Uri,
                                                               content_type= 'text/csv'))
        
        wf_instance_type = ParameterString(name="InstanceType", default_value=self.wf_instance_type)
        wf_instance_count = ParameterInteger(name="InstanceCount", default_value=self.wf_instance_count)
        pipeline_name = f"pipeline-{flow_export_name}"
        pipeline_steps = [data_wrangler_step, transform_step]

        pipeline = Pipeline(
            name=pipeline_name,
            parameters=[wf_instance_type, wf_instance_count],
            steps=pipeline_steps,
            sagemaker_session=sess
        )

        pipeline.upsert(role_arn=iam_role)
        return pipeline