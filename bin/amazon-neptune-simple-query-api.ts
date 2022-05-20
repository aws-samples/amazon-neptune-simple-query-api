#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AmazonNeptuneSimpleQueryApiStack } from '../lib/amazon-neptune-simple-query-api-stack';

const app = new cdk.App();
new AmazonNeptuneSimpleQueryApiStack(app, 'AmazonNeptuneSimpleQueryApiStack');
