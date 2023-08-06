import datetime

import boto3
import pytz
from boto3 import session
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


__author__ = 'Klera DevOps'
__version__ = '0.1.0'


class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            if 'iam_role_to_assume' in kwargs.keys():
                self.iam_role_to_assume = kwargs['iam_role_to_assume']
                self.sts_client = boto3.client(
                    'sts',
                    aws_access_key_id=kwargs['aws_access_key_id'],
                    aws_secret_access_key=kwargs['aws_secret_access_key'],
                )
                self.creds = self.sts_client.assume_role(
                    RoleArn=self.iam_role_to_assume,
                    RoleSessionName='RecommenderSession',
                    DurationSeconds=3600
                )
                self.session = session.Session(
                    aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                    aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                    aws_session_token=self.creds['Credentials']['SessionToken']
                )
            else:
                self.session = session.Session(
                    aws_access_key_id=kwargs['aws_access_key_id'],
                    aws_secret_access_key=kwargs['aws_secret_access_key'],
                )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])
        elif 'iam_role_to_assume' in kwargs.keys():
            self.iam_role_to_assume = kwargs['iam_role_to_assume']
            self.sts_client = boto3.client('sts')
            self.creds = self.sts_client.assume_role(
                RoleArn=kwargs['iam_role_to_assume'],
                RoleSessionName='RecommenderSession',
                DurationSeconds=3600
            )
            self.session = session.Session(
                aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                aws_session_token=self.creds['Credentials']['SessionToken']
            )

    from .utils import get_regions, list_log_groups, list_rds_instances, list_rds_clusters, list_ec2_instances
    from .cloudwatch import log_group_encrypted, log_group_retention_period_check
    from .rds import rds_logging_enabled, rds_cluster_deletion_protection_enabled, rds_cluster_multi_az_enabled, \
        rds_instance_iam_authentication_enabled
    from .ec2 import ec2_instance_no_public_ip

    # refresh session
    def refresh_session(self):
        try:
            self.sts_client
        except AttributeError:
            logger.info('No need to refresh the session!')
            return
        remaining_duration_seconds = (
                self.creds['Credentials']['Expiration'] - datetime.datetime.now(pytz.utc)).total_seconds()
        if remaining_duration_seconds < 900:
            self.creds = self.sts_client.assume_role(
                RoleArn=self.iam_role_to_assume,
                RoleSessionName='RecommenderSession',
                DurationSeconds=3600
            )
            self.session = session.Session(
                aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                aws_session_token=self.creds['Credentials']['SessionToken']
            )

    def get_compliance(self) -> list:
        """
        :return:
        """
        regions = self.get_regions()

        compliance = []

        try:
            log_groups = self.list_log_groups(regions=regions)
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.log_group_encrypted(exception=True, exception_text=e.response['Error']['Code'])),
            compliance.append(self.log_group_retention_period_check(exception=True, exception_text=e.response['Error']['Code']))
        else:
            compliance.append(self.log_group_encrypted(log_groups=log_groups)),
            compliance.append(self.log_group_retention_period_check(log_groups=log_groups))

        try:
            rds_list = self.list_rds_instances(regions=regions)
            # print('rds instances')
            # print(rds_list)
        except ClientError as e:
            compliance.append(self.rds_instance_iam_authentication_enabled(exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.rds_logging_enabled(exception=True, exception_text=e.response['Error']['Code']))
        else:
            compliance.append(self.rds_instance_iam_authentication_enabled(rds_lst=rds_list))
            compliance.append(self.rds_logging_enabled(rds_lst=rds_list))

        try:
            rds_clusters = self.list_rds_clusters(regions=regions)
            # print('rds clusters')
            # print(rds_clusters)
        except ClientError as e:
            compliance.append(self.rds_cluster_deletion_protection_enabled(
                exception=True, exception_text=e.response['Error']['Code'])
            )
            compliance.append(self.rds_cluster_multi_az_enabled(
                exception=True, exception_text=e.response['Error']['Code'])
            )
        else:
            compliance.append(self.rds_cluster_deletion_protection_enabled(cluster_list=rds_clusters))
            compliance.append(self.rds_cluster_multi_az_enabled(cluster_list=rds_clusters))

        try:
            ec2_instances = self.list_ec2_instances(regions=regions)
            # print('ec2 instances')
            # print(ec2_instances)
        except ClientError as e:
            compliance.append(self.ec2_instance_no_public_ip(
                exception=True, exception_text=e.response['Error']['Code']))
        else:
            compliance.append(self.ec2_instance_no_public_ip(instances=ec2_instances))

        return compliance
