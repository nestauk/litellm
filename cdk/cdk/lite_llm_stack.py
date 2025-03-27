from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_p,
    aws_ecs as ecs,
    Stack,
)
from constructs import Construct

class LiteLLMStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Host VPC
        vpc = ec2.Vpc(self, "LiteLLMProxyVPC",
            max_azs=3,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                )
            ]
        )

        lite_llm_service = ecs_p.ApplicationLoadBalancedFargateService(self, "LiteLLMProxyService",
            cpu=256,
            desired_count=1,
            memory_limit_mib=512,
            task_image_options={
                "image": ecs.ContainerImage.from_registry(self.node.try_get_context("lite_llm_image")),
            },
            public_load_balancer=True,
            vpc=vpc,
            redirect_http=True,
        )

        lite_llm_service.service.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Internet access to the service (HTTP redirect)")
        lite_llm_service.service.connections.allow_from_any_ipv4(ec2.Port.tcp(443), "Internet access to the service")

        lite_llm_service.target_group.configure_health_check(
            path="/",
        )
