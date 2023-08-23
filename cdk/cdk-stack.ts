import {
  App,
  CfnOutput,
  Duration,
  Stack,
} from "aws-cdk-lib";
import * as path from "path";
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { DockerImageCode } from "aws-cdk-lib/aws-lambda";
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';
import { HttpApi, HttpMethod } from "@aws-cdk/aws-apigatewayv2-alpha";
import { HttpLambdaIntegration } from "@aws-cdk/aws-apigatewayv2-integrations-alpha";


const rootPath = path.join(__dirname, "..");

const app = new App();

const stack = new Stack(app, "IntutionStack", {
  env: {
    region: "eu-west-1",
    account: process.env.CDK_DEFAULT_ACCOUNT,
  },
});

const entry = path.join(rootPath, "lambda", "sentiment");


const lambdaFn = new lambda.DockerImageFunction(
    stack,
    "SentimentLambda",
    {
      code: DockerImageCode.fromImageAsset(entry),
      memorySize: 5120,
      timeout: Duration.minutes(15),
    }
  );

const sentimentIntegration =  new HttpLambdaIntegration('sentimentIntegration', lambdaFn)

const api = new HttpApi(stack, "SentimentApi");

api.addRoutes({
  path: '/qa',
  methods: [ HttpMethod.POST ],
  integration: sentimentIntegration,
});

new CfnOutput(stack, "SentimentEndpoint", {
  value: api.url || "",
});

