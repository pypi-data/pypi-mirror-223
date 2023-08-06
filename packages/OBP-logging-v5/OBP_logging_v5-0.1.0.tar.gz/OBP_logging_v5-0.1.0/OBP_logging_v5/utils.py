import logging

import botocore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_regions(self):
    logger.info(" ---Inside utils :: get_regions()--- ")
    self.refresh_session()
    """Summary

    Returns:
        TYPE: Description
    """

    client = self.session.client('ec2', region_name='us-east-1')
    region_response = {}
    try:
        region_response = client.describe_regions()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AuthFailure':
            logger.error(f" AccessKey credentails not found here: {error}")
            exit(1)
    except botocore.exceptions.NoCredentialsError as e:
        logger.error(f" Unable to locate credentials: {e} ")
        exit(1)

    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions


# returns the list of log groups
def list_log_groups(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_log_groups()--- ")
    self.refresh_session()

    log_groups = {}

    for region in regions:
        # Connect to the cloudwatch log service
        client = self.session.client('logs', region_name=region)
        marker = ''
        while True:
            # list all log groups
            if marker == '':
                response = client.describe_log_groups()
            else:
                response = client.describe_log_groups(
                    nextToken=marker
                )
            # adding the list of log groups to the log_groups
            log_groups.setdefault(region, []).extend(response['logGroups'])

            # trying to fetch the nextToken
            try:
                marker = response['nextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return log_groups


# returns the list of rds instances
def list_rds_instances(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_instances()--- ")
    self.refresh_session()
    rds_list = {}

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_instances()
            else:
                response = client.describe_db_instances(
                    Marker=marker
                )
            rds_list.setdefault(region, []).extend(response['DBInstances'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return rds_list


# return the list of rds clusters
def list_rds_clusters(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_clusters()--- ")
    self.refresh_session()

    cluster_lst = {}

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_clusters()
            else:
                response = client.describe_db_clusters(
                    Marker=marker
                )
            cluster_lst.setdefault(region, []).extend(response['DBClusters'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return cluster_lst


# returns the list of ec2 instances
def list_ec2_instances(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_ec2_instances()--- ")
    self.refresh_session()

    instances = {}

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_instances()
            else:
                response = client.describe_instances(
                    NextToken=marker
                )
            instances.setdefault(region, []).extend(response['Reservations'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return instances
