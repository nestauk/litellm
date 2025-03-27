#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk.cdk.lite_llm_stack import LiteLLMStack


app = cdk.App()

# Specifically done for this proof of concept, as it's easier to integrate
# secrets. I'll port it to Terraform at some point.
LiteLLMStack(app, "lite-llm-proxy",
    env=cdk.Environment(account='442426849750', region='eu-west-2'),
    )

app.synth()
