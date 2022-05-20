# Amazon Neptune Simple Query API

This repository shows how to expose your gremlin API using Amazon Neptune. The backend provides PYMK (People You May Know) recommendation API. The social network is created by [aws-samples/amazon-neptune-samples](https://github.com/aws-samples/amazon-neptune-samples/blob/master/neptune-sagemaker/notebooks/Getting-Started/03-Social-Network-Recommendations.ipynb) Jupyter Notebook. This project provides a lambda function which can load the social network to Neptune by just invoking once. If you would like to know more about the social network and PYMK, refer to the original notebook.

## Amazon Neptune Deployment by AWS CDK

### Pre-requirements
- Bash
- Node.js
- Docker
- Configured AWS account (Attach AdministratorAccess policy is recommended)
- `aws` command line tool

### Deployment

Install the dependencies first.
```bash
npm install
```

If it is a first time you try AWS CDK, you need to bootstrap your AWS account.
Execute command below. (If the account was already bootstrapped, skip the step.)
```bash
npx cdk bootstrap
```

Execute deployment by the command below.
```bash
npx cdk deploy
```

## Loading Social Networks

This is the visualized social network graph which will be created.

![](/imgs/03-social-network.png)

Invoke a lambda function once by the command below. It'll load the social network to the Neptune database.
```bash
# Fetch a function name by the output of the CloudFormation stack
FUNCTION_NAME=$(
    aws cloudformation describe-stacks \
        --stack-name "AmazonNeptuneSimpleQueryApiStack" \
        --query "Stacks[0].Outputs[?OutputKey=='LoadSocialNetworkFunctionName'].OutputValue" \
        --output text
)

# Invoke the function
aws lambda invoke \
    --function-name $FUNCTION_NAME \
    --invocation-type Event \
    out --lot-type Tail
```

## Try API

Execute `curl` to call the api. It'll fetch the PYMK of Terry. Replace the `<REPLACE_IT>` placeholders.
```bash
curl https://<REPLACE_IT (ID)>.execute-api.<REPLACE_IT (Region)>.amazonaws.com/prod/pymk?target_user=Terry
```

## Cleanup

Cleaning up the environment by the command below.
```bash
npx cdk destroy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
