# Snowflake + Amazon SageMaker Workshops

## Loan Default Workshop

In this workshop you'll learn how to facilitate a data-centric AI development process using Snowflake and Amazon SageMaker. In the workshop you will build a loan default model on personal loans data dervied from the Lending Club. As part of a iterative process we'll improve our dataset by enriching it with unemployment rate data provided by Knoema.

### Environment Setup
#### With Amazon SageMaker Studio
Use this template if you do not have a pre-existing Amazon SageMaker Studio environment in your target region.

Region name | Region code | Launch
--- | --- | ---
US East (N. Virginia) | us-east-1 | [![With Amazon SageMaker Studio](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-w-studio.yml")
US West (Oregon)| us-west-2 | [![With Amazon SageMaker Studio](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-w-studio.yml")
Europe (Ireland) | eu-west-1 | [![With Amazon SageMaker Studio](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-w-studio.yml")
Asia Pacific (Tokyo) | ap-northeast-1 | [![With Amazon SageMaker Studio](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-w-studio.yml")
Asia Pacific (Sydney) | ap-southeast-2 | [![With Amazon SageMaker Studio](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-w-studio.yml")

#### Use Existing Amazon SageMaker Studio Environment
Use this template if you have an Amazon SageMaker Studio deployed in your target region.

Region name | Region code | Launch
--- | --- | ---
US East (N. Virginia) | us-east-1 | [![Existing SageMaker Studio Environment](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-no-studio.yml)
US West (Oregon)| us-west-2 | [![Existing SageMaker Studio Environment](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-no-studio.yml)
Europe (Ireland) | eu-west-1 | [![Existing SageMaker Studio Environment](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-no-studio.yml)
Asia Pacific (Tokyo) | ap-northeast-1 | [![Existing SageMaker Studio Environment](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-no-studio.yml)
Asia Pacific (Sydney) | ap-southeast-2 | [![Existing SageMaker Studio Environment](/images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=snowflake-sagemaker-credit-risk-workshop&templateURL=https://snowflake-corp-se-workshop.s3.us-west-1.amazonaws.com/VHOL_Snowflake_Data_Wrangler/V2/cft/workshop-setup-no-studio.yml)
