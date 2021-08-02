# Snowflake + Amazon SageMaker Workshops [BETA]

The workshop assets in this repository are currently in **BETA**. We're currently working on simplifying the setup process. Reach out to dylatong@amazon.com if you have feeedback.


### Loan Default Workshop
----

1. **Environment Setup:**

    | Option | Description | Launch Template |
    |--------|-------------|-----------------|
    | **With Amazon SageMaker Studio** | Use this template if you do not have a pre-existing Amazon SageMaker Studio environment in your target region. | <a href="https://console.aws.amazon.com/cloudformation/home?region=region#/stacks/new?stackName=kernel-builder&templateURL=https://dtong-public-fileshare.s3.us-west-2.amazonaws.com/snowflake-sagemaker-workshop/src/deploy/cf/workshop-setup-w-studio.yml">![With Amazon SageMaker Studio](/images/deploy-to-aws.png)</a> |
    | **Use Existing Amazon SageMaker Studio Environment** | Use this template if you have an Amazon SageMaker Studio deployed in your target region. | <a href="https://console.aws.amazon.com/cloudformation/home?region=region#/stacks/new?stackName=kernel-builder&templateURL=https://dtong-public-fileshare.s3.us-west-2.amazonaws.com/snowflake-sagemaker-workshop/src/deploy/cf/workshop-setup-no-studio.yml">![Existing SageMaker Studio Environment](/images/deploy-to-aws.png)</a> |
