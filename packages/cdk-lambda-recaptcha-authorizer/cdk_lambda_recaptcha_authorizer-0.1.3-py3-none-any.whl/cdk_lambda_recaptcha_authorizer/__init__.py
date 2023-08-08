'''
# ReCaptcha Authorizer for AWS CDK

This is an AWS CDK construct that provides an easy way to add ReCaptcha-based authorization
to your API Gateway endpoints. It uses Google's ReCaptcha API to verify user responses and
secure your API resources.

## Installation

To use this construct in your AWS CDK projects, you can install it from npm:

```bash
npm install cdk-lambda-recaptcha-authorizer
```

## Example Usage

Here's an example of how to use the `ReCaptchaAuthorizer` construct in your AWS CDK stack:

```python
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { ReCaptchaAuthorizer } from 'cdk-lambda-recaptcha-authorizer';

export class ExampleRecaptchaAuthorizerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const api = new apigw.RestApi(this, 'Api', {
      restApiName: 'API',
      description: 'API with reCAPTCHA authorizer',
    });

    // Create the ReCaptchaAuthorizer and provide your ReCaptcha secret key
    const reCaptchaAuthorizer = new ReCaptchaAuthorizer(this, 'ReCaptchaAuthorizer', {
      reCaptchaSecretKey: 'YOUR_RECAPTCHA_SECRET_KEY',
      reCaptchaVersion: 'v2', // Use 'v2' or 'v3'
      // v3MinScoreRequired?: 0.5, // (Optional) Minimum score required for ReCaptcha v3
      // v3Action?: 'your_custom_action', // (Optional) Specify a custom action for ReCaptcha v3
      // challangeResponseHeaderName?: 'X-Recaptcha-Response', // (Optional) Custom header name for ReCaptcha token
    });

    // Create an API Gateway resource and associate the ReCaptchaAuthorizer with it
    const resource = api.root.addResource('hello');
    resource.addMethod('GET', new apigw.LambdaIntegration(new lambda.Function(this, 'Lambda', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline('exports.handler = async () => { return { statusCode: 200, body: "Hello World!" }; };'),
    })), {
      authorizer: reCaptchaAuthorizer.authorizer,
      authorizationType: apigw.AuthorizationType.CUSTOM,
    });
  }
}
```

## Configuration

The `ReCaptchaAuthorizer` accepts the following configuration options:

* `reCaptchaSecretKey`: Your ReCaptcha secret key. It is required.
* `reCaptchaVersion`: The ReCaptcha version to use. It can be either 'v2' or 'v3'.
* `v3MinScoreRequired`: (Optional) The minimum score required for ReCaptcha v3 authorization. Default is 0.5.
* `v3Action`: (Optional) Specify a custom action name for ReCaptcha v3 authorization.
* `challangeResponseHeaderName`: (Optional) The name of the header containing the
  ReCaptcha response token. Default is 'X-Recaptcha-Response'.

The `reCaptchaSecretKey` and `reCaptchaVersion` are mandatory parameters, as they are essential
for the ReCaptcha verification process. If you don't provide these values, an error will be thrown.

For ReCaptcha v3, you can optionally set the `v3MinScoreRequired` parameter to specify the minimum
score required for authorization. The default value is 0.5, but you can adjust it as needed.

If you are using ReCaptcha v3 and have defined specific actions in your ReCaptcha settings,
you can use the `v3Action` parameter to specify the expected action name for the request.
If the action name doesn't match the one provided, the verification will fail.

Additionally, you can customize the header name used to send the ReCaptcha token
with the `challangeResponseHeaderName` parameter. The default header name is 'X-Recaptcha-Response',
but you can use a custom name if needed.

Keep in mind that these configuration options should be provided when creating the `ReCaptchaAuthorizer`
instance to ensure proper functioning and security of your API endpoints.

## How It Works

The `ReCaptchaAuthorizer` construct creates an AWS Lambda function that handles the ReCaptcha verification.
It sends the ReCaptcha token to Google's ReCaptcha API using an HTTPS POST request and verifies
the user's response. If the verification is successful, the authorizer allows the request to proceed
and grants access to the associated API Gateway resource.

Here's a high-level overview of the process:

1. When a client makes a request to an API Gateway endpoint protected by the `ReCaptchaAuthorizer`,
   it includes a ReCaptcha token in the request headers.
2. The `ReCaptchaAuthorizer` Lambda function receives the request and extracts the ReCaptcha
   token from the headers.
3. The Lambda function then sends an HTTPS POST request to Google's ReCaptcha API with the
   ReCaptcha token and your ReCaptcha secret key.
4. Google's ReCaptcha API verifies the token and sends back a response indicating whether
   the token is valid or not.
5. If the ReCaptcha token is valid, the Lambda function allows the request to proceed
   and grants access to the API Gateway resource.
6. If the ReCaptcha token is invalid or the verification fails, the Lambda function
   denies access to the API Gateway resource and returns an unauthorized response.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-lambda-recaptcha-authorizer.IReCaptchaAuthorizerProps")
class IReCaptchaAuthorizerProps(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="reCaptchaSecretKey")
    def re_captcha_secret_key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @re_captcha_secret_key.setter
    def re_captcha_secret_key(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="reCaptchaVersion")
    def re_captcha_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @re_captcha_version.setter
    def re_captcha_version(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="challangeResponseHeaderName")
    def challange_response_header_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @challange_response_header_name.setter
    def challange_response_header_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="v3Action")
    def v3_action(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @v3_action.setter
    def v3_action(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="v3MinScoreRequired")
    def v3_min_score_required(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        ...

    @v3_min_score_required.setter
    def v3_min_score_required(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IReCaptchaAuthorizerPropsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-lambda-recaptcha-authorizer.IReCaptchaAuthorizerProps"

    @builtins.property
    @jsii.member(jsii_name="reCaptchaSecretKey")
    def re_captcha_secret_key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "reCaptchaSecretKey"))

    @re_captcha_secret_key.setter
    def re_captcha_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7780121939ac4a770ef2be6a1333c356b8435b400e83aeb717f3f9e04b035c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reCaptchaSecretKey", value)

    @builtins.property
    @jsii.member(jsii_name="reCaptchaVersion")
    def re_captcha_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "reCaptchaVersion"))

    @re_captcha_version.setter
    def re_captcha_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e234ae4bfc2d9f45c7f4ef16526e9dfe9aca5d024d55b9193f976eccb0e87ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reCaptchaVersion", value)

    @builtins.property
    @jsii.member(jsii_name="challangeResponseHeaderName")
    def challange_response_header_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "challangeResponseHeaderName"))

    @challange_response_header_name.setter
    def challange_response_header_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c248acdb87a9d991387cadce721f9ae901c6c9c8c1cda4e078af98d191d687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "challangeResponseHeaderName", value)

    @builtins.property
    @jsii.member(jsii_name="v3Action")
    def v3_action(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "v3Action"))

    @v3_action.setter
    def v3_action(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0eca27c32f002bf6d024b5d2e433d4593b8f7f74f318e6bb1872c9dcc5563e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "v3Action", value)

    @builtins.property
    @jsii.member(jsii_name="v3MinScoreRequired")
    def v3_min_score_required(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "v3MinScoreRequired"))

    @v3_min_score_required.setter
    def v3_min_score_required(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6187176637344de7fafd24f02ddac3fe9230e98080ff0bb06861cf587fa34d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "v3MinScoreRequired", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReCaptchaAuthorizerProps).__jsii_proxy_class__ = lambda : _IReCaptchaAuthorizerPropsProxy


class ReCaptchaAuthorizer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-recaptcha-authorizer.ReCaptchaAuthorizer",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IReCaptchaAuthorizerProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b92147e87efd304b41a314930a9f13bece7b0666b81bcfd1b4dd14d86a03a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authorizer")
    def authorizer(self) -> _aws_cdk_aws_apigateway_ceddda9d.RequestAuthorizer:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RequestAuthorizer, jsii.get(self, "authorizer"))


__all__ = [
    "IReCaptchaAuthorizerProps",
    "ReCaptchaAuthorizer",
]

publication.publish()

def _typecheckingstub__7780121939ac4a770ef2be6a1333c356b8435b400e83aeb717f3f9e04b035c54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e234ae4bfc2d9f45c7f4ef16526e9dfe9aca5d024d55b9193f976eccb0e87ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c248acdb87a9d991387cadce721f9ae901c6c9c8c1cda4e078af98d191d687(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0eca27c32f002bf6d024b5d2e433d4593b8f7f74f318e6bb1872c9dcc5563e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6187176637344de7fafd24f02ddac3fe9230e98080ff0bb06861cf587fa34d(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b92147e87efd304b41a314930a9f13bece7b0666b81bcfd1b4dd14d86a03a6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IReCaptchaAuthorizerProps,
) -> None:
    """Type checking stubs"""
    pass
