#!/usr/bin/env python

__author__ = "Dylan Tong"
__credits__ = ["Dylan Tong"]
__license__ = "Apache"
__version__ = "0.1"
__maintainer__ = "Dylan Tong"
__email__ = "dylatong@amazon.com"
__status__ = "Prototype"

def get_algorithm_arn(region, algo_name):
    acct_mapping = {
        "ap-northeast-1" : "977537786026",
        "ap-northeast-2" : "745090734665",
        "ap-southeast-1" : "192199979996",
        "ap-southeast-2" : "666831318237",
        "us-east-1"      : "865070037744",
        "eu-central-1"   : "446921602837",
        "ap-south-1"     : "077584701553",
        "sa-east-1"      : "270155090741",
        "ca-central-1"   : "470592106596",
        "eu-west-1"      : "985815980388",
        "eu-west-2"      : "856760150666",
        "eu-west-3"      : "843114510376",
        "eu-north-1"     : "136758871317",
        "us-west-1"      : "382657785993",
        "us-east-2"      : "057799348421",
        "us-west-2"      : "594846645681"
    }
        
    return "arn:aws:sagemaker:{}:{}:algorithm/{}".format(region, acct_mapping[region], algo_name)