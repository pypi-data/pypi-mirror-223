import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-lambda-recaptcha-authorizer",
    "version": "0.1.3",
    "description": "Custom construct for AWS CDK that provides an easy way to integrate reCAPTCHA-based authorization with Amazon API Gateway.",
    "license": "MIT",
    "url": "https://github.com/ilkerdagli/cdk-lambda-recaptcha-authorizer.git",
    "long_description_content_type": "text/markdown",
    "author": "Ilker Dagli<daglilker@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/ilkerdagli/cdk-lambda-recaptcha-authorizer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_lambda_recaptcha_authorizer",
        "cdk_lambda_recaptcha_authorizer._jsii"
    ],
    "package_data": {
        "cdk_lambda_recaptcha_authorizer._jsii": [
            "cdk-lambda-recaptcha-authorizer@0.1.3.jsii.tgz"
        ],
        "cdk_lambda_recaptcha_authorizer": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.86.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
