#!/usr/bin/env python

import json
import os
import subprocess
from re import search

import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import seaborn as sns

import pandas as pd
import numpy as np
#import shap
from sklearn.metrics import confusion_matrix

import boto3
from sagemaker.s3 import S3Downloader
        
__author__ = "Dylan Tong"
__credits__ = ["Dylan Tong"]
__license__ = "Apache"
__version__ = "0.1"
__maintainer__ = "Dylan Tong"
__email__ = "dylatong@amazon.com"
__status__ = "Prototype"

class ModelInspector() :

    PAGINATION_SIZE = 100
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def get_inspector(cls, config) :
    
        if not cls._instance :
            cls._instance = cls.__new__(cls)
        
        cls.bucket = config["workspace"]
        cls.results_prefix = config["prefixes"]["results_path"]
        cls.bias_prefix = config["prefixes"]["bias_path"]
        cls.xai_prefix = config["prefixes"]["xai_path"]
        
        cls.gt_idx = config["results-config"]["gt_index"]
        cls.pred_idx = config["results-config"]["pred_index"]

        db_driver = config["drivers"]["db"]
        dsmlp_driver = config["drivers"]["dsmlp"]
        cls.db = boto3.client("s3") if not db_driver else db_driver
        cls.dsmlp = boto3.client("sagemaker") if not dsmlp_driver else dsmlp_driver
                
        cls.results_df = cls._get_merged_df(cls.bucket, cls.results_prefix)
        
        return cls._instance 
    
    def get_results(self) :
        return self.results_df
    
    @classmethod
    def _get_merged_df(cls, bucket, prefix, has_header=True, maxkeys=10) :
        
        files = []
        skip = 0
        kwargs = {'Bucket': bucket, 'Prefix': prefix, 'MaxKeys': maxkeys}
        resp = cls.db.list_objects_v2(**kwargs)
        for obj in resp['Contents'] :
            
            if (has_header) :
                skip = 1

            files.append(pd.read_csv("s3://{}/{}".format(bucket, obj["Key"]), skiprows=skip, header=None))
                
        df = pd.concat(files)

        return df
    
    #def get_roc_curve(self, gt_index=0, pred_index=1, display=True, model_name="autopilot-model") :
    #        
    #    y = self._y()
    #    yh = self._yh()
        
    #    fpr, tpr, thresholds = roc_curve(y, yh)
    #    roc_auc = auc(fpr, tpr)

    #    viz = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name=model_name) 

    #    if display :
    #        viz.plot()
            
    #    return viz, roc_auc, fpr, tpr, thresholds
        
    def visualize_auc(self, fpr, tpr, thresholds) :
        
        df = pd.DataFrame({
            "False Positive Rate":fpr,
            "True Positive Rate":tpr,
            "Threshold":thresholds
        })

        axes = df.plot.area(stacked=False, x="Threshold", figsize=(20,3),colormap='RdGy', alpha=0.3)
        axes.set_xlabel("Threshold")
        axes.set_ylabel("Rate")
        axes.set_xlim(0,1.0)
        axes.set_ylim(0,1.0)
        
    def _y(self) :
        return self.results_df[self.gt_idx]
    
    def _yh(self) :
        return self.results_df[self.pred_idx]
    
    def display_interactive_cm(self, start=0.5, min=0.0, max=1.0, step=0.05) :

        y = self._y()
        yh = self._yh()
        
        def cm_heatmap_fn(Threshold) :

            cm = confusion_matrix(y, yh >= Threshold).astype(int)

            names = ['True Neg','False Pos','False Neg','True Pos']
            counts = ["{0:0.0f}".format(value)
                            for value in cm.flatten()]

            pcts = ["{0:.2%}".format(value)
                                 for value in cm.flatten()/np.sum(cm)]

            labels = [f"{v1}\n{v2}\n{v3}"
                      for v1, v2, v3 in zip(names,counts,pcts)]

            labels = np.asarray(labels).reshape(2,2)
            sns.heatmap(cm, annot=labels, fmt='', cmap='Blues')

        thresh_slider = widgets.FloatSlider(value=start,
                                            min=min,
                                            max=max,
                                            step=step)

        interact(cm_heatmap_fn, Threshold=thresh_slider)
        
    def _download_clarify_xai_summary(self) :
        
        try :
    
            summary_uri = f"s3://{self.bucket}/{self.xai_prefix}/analysis.json"
            S3Downloader.download(summary_uri, os.getcwd())

            with open('analysis.json', 'r') as f:
                summary = json.loads(f.read())

            return summary
    
        except Exception as e:
            print(f"{e}: Failed to download {xai_summary}")
            
    
    #def explain_prediction(self, data_row_id) :
    
    #    xai_summary = self._download_clarify_xai_summary()
        
    #    columns = list(xai_summary['explanations']['kernel_shap']['label0']["global_shap_values"].keys())
    #    xai_results = f"s3://{self.bucket}/{self.xai_prefix}/explanations_shap/out.csv"
    #    shap_df = pd.read_csv(xai_results)

    #    y = self._y()
    #    yh = self._yh()
        
    #    descr = f"The ground truth was {y.iloc[data_row_id]}. The model predicts "
    #    pred = yh.iloc[data_row_id]
    #    descr+= "{:3f}. \n".format(pred) if isinstance(pred, float) else f"{pred}. \n"
        
    #    expected_value = xai_summary['explanations']['kernel_shap']['label0']['expected_value']
    #    shap.force_plot(expected_value, np.array(shap_df.iloc[data_row_id,:]), np.array(columns), matplotlib=True)
        
    #    return descr
    
    @classmethod
    def _gt(cls, a,b) : return a > b
    @classmethod
    def _gte(cls, a,b) : return a >= b
    @classmethod
    def _lt(cls, a,b) : return a < b
    @classmethod
    def _lte(cls, a,b) : return a <= b
    @classmethod
    def _get_comparator(cls, maximize_objective=True) :    
        return cls._gte if maximize_objective else cls._lte
    
    def _init_baseline_summary(self, ids) :

        baselines = {}
        for i in ids :
            baselines[i] = {"value": None}
        return baselines

    def get_automl_job_baseline(self, job_name, candidate_ids, maximize_objective=True) :
        
        comparator = self._get_comparator(maximize_objective)
        baselines = self._init_baseline_summary(candidate_ids)

        trial_details = self.dsmlp.list_candidates_for_auto_ml_job(
                                    AutoMLJobName=job_name,
                                    StatusEquals="Completed",
                                    MaxResults=ModelInspector.PAGINATION_SIZE)
        while True :

            candidates = trial_details["Candidates"]
            for c in candidates :
                
                steps = c["CandidateSteps"]
                for s in steps :
                    for i in candidate_ids :
                        
                        if s["CandidateStepType"] == "AWS::SageMaker::TrainingJob" and search(i, s["CandidateStepName"]) :
                            metric = c['FinalAutoMLJobObjectiveMetric']['Value']      
                            if not baselines[i]["value"] or comparator(metric, baselines[i]["value"]) :
                                baselines[i]["metric"] = c['FinalAutoMLJobObjectiveMetric']['MetricName']
                                baselines[i]["value"] = metric

            if "NextToken" not in trial_details :
                break

            next_token = trial_details["NextToken"]
            trial_details = self.dsmlp.list_candidates_for_auto_ml_job(
                                AutoMLJobName = job_name,
                                StatusEquals = "Completed",
                                MaxResults = ModelInspector.PAGINATION_SIZE,
                                NextToken = next_token)
            
        return baselines
    
    def get_aws_cli_query_for_baselines(self, job_name, candidate_id) :
        
        jmespath_query = "max_by(Candidates[].{step_name:CandidateSteps[?CandidateStepType == 'AWS::SageMaker::TrainingJob'].CandidateStepName[?contains(@,'"+candidate_id+"')==\`true\`],obj_value:FinalAutoMLJobObjectiveMetric.Value}[?not_null(step_name)], &obj_value)"
        
        cmd = "aws sagemaker list-candidates-for-auto-ml-job --auto-ml-job-name {} --query \"{}\"".format(job_name,jmespath_query)
        
        stdout = subprocess.check_output(cmd, shell=True)
        
        return (cmd, json.loads(stdout))
