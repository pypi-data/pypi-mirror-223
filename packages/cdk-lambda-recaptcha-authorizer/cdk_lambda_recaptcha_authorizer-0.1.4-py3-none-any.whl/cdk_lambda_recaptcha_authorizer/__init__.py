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

export class LraExampleStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const challangeResponseHeaderName = 'X-My-Header'

    const api = new apigw.RestApi(this, 'Api', {
      restApiName: 'API',
      description: 'API with reCAPTCHA authorizer',
      defaultCorsPreflightOptions: {
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          challangeResponseHeaderName
        ],
        allowCredentials: true,
        allowOrigins: ['*'],
        allowMethods: ['OPTIONS', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
      }
    });

    const reCaptchaAuthorizer = new ReCaptchaAuthorizer(this, 'ReCaptchaAuthorizer', {
      reCaptchaSecretKey: 'YOUR-RECAPTCHA-SECRET-KEY',
      reCaptchaVersion: 'v2',
      challangeResponseHeaderName: challangeResponseHeaderName
    })

    const resource = api.root.addResource('submitForm');

    resource.addMethod('POST', new apigw.LambdaIntegration(new lambda.Function(this, 'Lambda', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline('exports.handler = async () => { return { statusCode: 200, body: "Hello World!" }; };'),
    })), {

      authorizer: reCaptchaAuthorizer,
      authorizationType: apigw.AuthorizationType.CUSTOM,
    });
  }
}
```

Here's an example form in html that sends recaptcha challange response in header:

```html
<!DOCTYPE html>
<html>
   <head>
      <title>reCAPTCHA v2 Demo</title>
      <script src="https://www.google.com/recaptcha/api.js" async defer></script>
   </head>
   <body>
      <h1>reCAPTCHA v2 Demo Form</h1>
      <form
         id="demoForm"
         method="POST"
         >
         <label for="name">Name:</label>
         <input type="text" id="name" name="name" required />
         <br />
         <div class="g-recaptcha" data-sitekey="YOUR-RECAPTCHA-SITE-KEY"></div>
         <button type="submit">Submit</button>
      </form>
      <script>
         const form = document.getElementById("demoForm")

         form.addEventListener("submit", async (event) => {
           event.preventDefault()
           const recaptchaResponse = grecaptcha.getResponse()

           if (recaptchaResponse === "") {
             alert("Please complete the reCAPTCHA verification.")
             return
           }

           const headers = new Headers()
           headers.append("X-My-Header", recaptchaResponse)

           const response = await fetch("YOUR-API-GATEWAY-URL", {
             method: "POST",
             headers: headers,
             body: new FormData(form),
           })

           if (response.ok) {
             alert("Form submitted successfully!")
           } else {
             alert("Form submission failed. Please try again later.")
           }
         })
      </script>
   </body>
</html>
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


@jsii.implements(_aws_cdk_aws_apigateway_ceddda9d.IAuthorizer)
class ReCaptchaAuthorizer(
    _aws_cdk_aws_apigateway_ceddda9d.Authorizer,
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
        *,
        re_captcha_secret_key: builtins.str,
        re_captcha_version: builtins.str,
        challange_response_header_name: typing.Optional[builtins.str] = None,
        v3_action: typing.Optional[builtins.str] = None,
        v3_min_score_required: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param re_captcha_secret_key: 
        :param re_captcha_version: 
        :param challange_response_header_name: 
        :param v3_action: 
        :param v3_min_score_required: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b92147e87efd304b41a314930a9f13bece7b0666b81bcfd1b4dd14d86a03a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ReCaptchaAuthorizerProps(
            re_captcha_secret_key=re_captcha_secret_key,
            re_captcha_version=re_captcha_version,
            challange_response_header_name=challange_response_header_name,
            v3_action=v3_action,
            v3_min_score_required=v3_min_score_required,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authorizer")
    def authorizer(self) -> _aws_cdk_aws_apigateway_ceddda9d.RequestAuthorizer:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RequestAuthorizer, jsii.get(self, "authorizer"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        '''(experimental) The authorizer ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))


@jsii.data_type(
    jsii_type="cdk-lambda-recaptcha-authorizer.ReCaptchaAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "re_captcha_secret_key": "reCaptchaSecretKey",
        "re_captcha_version": "reCaptchaVersion",
        "challange_response_header_name": "challangeResponseHeaderName",
        "v3_action": "v3Action",
        "v3_min_score_required": "v3MinScoreRequired",
    },
)
class ReCaptchaAuthorizerProps:
    def __init__(
        self,
        *,
        re_captcha_secret_key: builtins.str,
        re_captcha_version: builtins.str,
        challange_response_header_name: typing.Optional[builtins.str] = None,
        v3_action: typing.Optional[builtins.str] = None,
        v3_min_score_required: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param re_captcha_secret_key: 
        :param re_captcha_version: 
        :param challange_response_header_name: 
        :param v3_action: 
        :param v3_min_score_required: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03df3d2de02c9602312fd3c7395d364c04abfebd128fc9ee58d9c3363ffedbe9)
            check_type(argname="argument re_captcha_secret_key", value=re_captcha_secret_key, expected_type=type_hints["re_captcha_secret_key"])
            check_type(argname="argument re_captcha_version", value=re_captcha_version, expected_type=type_hints["re_captcha_version"])
            check_type(argname="argument challange_response_header_name", value=challange_response_header_name, expected_type=type_hints["challange_response_header_name"])
            check_type(argname="argument v3_action", value=v3_action, expected_type=type_hints["v3_action"])
            check_type(argname="argument v3_min_score_required", value=v3_min_score_required, expected_type=type_hints["v3_min_score_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "re_captcha_secret_key": re_captcha_secret_key,
            "re_captcha_version": re_captcha_version,
        }
        if challange_response_header_name is not None:
            self._values["challange_response_header_name"] = challange_response_header_name
        if v3_action is not None:
            self._values["v3_action"] = v3_action
        if v3_min_score_required is not None:
            self._values["v3_min_score_required"] = v3_min_score_required

    @builtins.property
    def re_captcha_secret_key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("re_captcha_secret_key")
        assert result is not None, "Required property 're_captcha_secret_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def re_captcha_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("re_captcha_version")
        assert result is not None, "Required property 're_captcha_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def challange_response_header_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("challange_response_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def v3_action(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("v3_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def v3_min_score_required(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("v3_min_score_required")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReCaptchaAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ReCaptchaAuthorizer",
    "ReCaptchaAuthorizerProps",
]

publication.publish()

def _typecheckingstub__77b92147e87efd304b41a314930a9f13bece7b0666b81bcfd1b4dd14d86a03a6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    re_captcha_secret_key: builtins.str,
    re_captcha_version: builtins.str,
    challange_response_header_name: typing.Optional[builtins.str] = None,
    v3_action: typing.Optional[builtins.str] = None,
    v3_min_score_required: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03df3d2de02c9602312fd3c7395d364c04abfebd128fc9ee58d9c3363ffedbe9(
    *,
    re_captcha_secret_key: builtins.str,
    re_captcha_version: builtins.str,
    challange_response_header_name: typing.Optional[builtins.str] = None,
    v3_action: typing.Optional[builtins.str] = None,
    v3_min_score_required: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
