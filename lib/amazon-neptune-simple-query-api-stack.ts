import { Stack, StackProps, Duration, Token, CfnOutput } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { CfnDBCluster, CfnDBInstance, CfnDBSubnetGroup } from 'aws-cdk-lib/aws-neptune';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as _lambda from 'aws-cdk-lib/aws-lambda';
import * as lambda from '@aws-cdk/aws-lambda-python-alpha';
import * as agw from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';

export class AmazonNeptuneSimpleQueryApiStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'NeptuneVpc');
    const privateSubnets = vpc.selectSubnets({
      subnetType: ec2.SubnetType.PRIVATE,
    });

    const securityGroup = new ec2.SecurityGroup(this, 'NeptuneSecurityGroup', {
      vpc,
    });
    securityGroup.addIngressRule(ec2.Peer.ipv4(vpc.vpcCidrBlock), ec2.Port.tcp(8182));

    const neptuneSubnetGroup = new CfnDBSubnetGroup(this, 'NeptuneSubnet', {
      dbSubnetGroupDescription: 'Neptune private subnets',
      subnetIds: privateSubnets.subnetIds,
    });

    const neptuneCluster = new CfnDBCluster(this, 'NeptuneCluster', {
      engineVersion: '1.1.0.0',
      dbSubnetGroupName: neptuneSubnetGroup.ref,
      vpcSecurityGroupIds: [securityGroup.securityGroupId],
      storageEncrypted: true,
    });

    const neptuneInstance = new CfnDBInstance(this, 'NeptuneInstance', {
      dbInstanceClass: 'db.r5.xlarge',
      dbClusterIdentifier: neptuneCluster.ref,
    });

    const commonLambdaProps = {
      runtime: _lambda.Runtime.PYTHON_3_9,
      entry: path.join(__dirname, '..', 'lambda'),
      timeout: Duration.minutes(15),
      environment: {
        NEPTUNE_DOMAIN: Token.asString(neptuneInstance.getAtt('Endpoint')),
      },
      vpc,
    };

    const loadSocialNetwork = new lambda.PythonFunction(this, 'LoadSocialNetwork', {
      ...commonLambdaProps,
      index: 'load_social_network.py',
    });

    const pymk = new lambda.PythonFunction(this, 'Pymk', {
      ...commonLambdaProps,
      index: 'pymk.py',
    });

    const api = new agw.RestApi(this, 'RestApi', {
      defaultCorsPreflightOptions: {
        allowOrigins: agw.Cors.ALL_ORIGINS,
        allowMethods: agw.Cors.ALL_METHODS
      },
    });

    api.addGatewayResponse('RestApi4xx', {
      type: agw.ResponseType.DEFAULT_4XX,
      responseHeaders: {
        'Access-Control-Allow-Origin': "'*'",
      },
    });

    api.addGatewayResponse('RestApi5xx', {
      type: agw.ResponseType.DEFAULT_5XX,
      responseHeaders: {
        'Access-Control-Allow-Origin': "'*'",
      },
    });

    const apiPymk = api.root.addResource('pymk');

    apiPymk.addMethod('GET', new agw.LambdaIntegration(pymk));

    new CfnOutput(this, 'LoadSocialNetworkFunctionName', {
      value: loadSocialNetwork.functionName,
    });
  }
}
