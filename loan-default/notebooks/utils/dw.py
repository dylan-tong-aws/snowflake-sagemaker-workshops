#!/usr/bin/env python

import boto3
from urllib.parse import urlparse

__author__ = "Dylan Tong"
__credits__ = ["Dylan Tong"]
__license__ = "Apache"
__version__ = "0.1"
__maintainer__ = "Dylan Tong"
__email__ = "dylatong@amazon.com"
__status__ = "Prototype"

client = boto3.client("s3")

def get_first_matching_s3_key(bucket, prefix=''):
            
    kwargs = {'Bucket': bucket, 'Prefix': prefix, 'MaxKeys': 1}
    resp = client.list_objects_v2(**kwargs)
    for obj in resp['Contents']:
        return obj['Key']
    
def get_data_uri(unique_s3_prefix) :
            
    parsed = urlparse(unique_s3_prefix, allow_fragments=False)
    if parsed.query:
        prefix= parsed.path.lstrip('/') + '?' + parsed.query
    else:
        prefix= parsed.path.lstrip('/')
    
    key = get_first_matching_s3_key(parsed.netloc, prefix)
    return f"s3://{parsed.netloc}/{key}"

def get_data_s3_prefix(unique_s3_prefix) :
    
    parsed = urlparse(unique_s3_prefix, allow_fragments=False)
    if parsed.query:
        prefix= parsed.path.lstrip('/') + '?' + parsed.query
    else:
        prefix= parsed.path.lstrip('/')
    
    return get_first_matching_s3_key(parsed.netloc, prefix)


def get_data_wrangler_container_uri(region, tag):

    image_name = "sagemaker-data-wrangler-container"
    account = {    
            "us-west-1" : "926135532090",
            "us-west-2" : "174368400705",
            "us-east-1" : "663277389841",
            "us-east-2" : "415577184552",
            "ap-east-1" : "707077482487",
            "ap-northeast-1" : "649008135260",
            "ap-northeast-2" : "131546521161",
            "ap-southeast-1" : "119527597002",
            "ap-southeast-2" : "422173101802",
            "ap-south-1" : "089933028263",
            "eu-west-1" : "245179582081",
            "eu-west-2" : "894491911112",
            "eu-west-3" : "807237891255",
            "eu-south-1": "488287956546",
            "eu-central-1" : "024640144536",
            "ca-central-1" : "557239378090",
            "af-south-1" : "143210264188",
            "sa-east-1" : "424196993095",
            "me-south-1" : "376037874950"
    }[region]

    if not account :
        raise Exception("No entry found. Export your flow manually from the Data Wrangler console and update the account \
                        mapping in this function.")

    return f"{account}.dkr.ecr.{region}.amazonaws.com/{image_name}:{tag}"