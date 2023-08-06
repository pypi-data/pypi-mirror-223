"""
Contains the methods to check compliance for rds
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance for rds logging enabled
def rds_logging_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside rds :: rds_logging_enabled()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.77'
    compliance_type = 'RDS Logging Enabled'
    description = 'Checks that respective logs of Amazon Relational Database Service (Amazon RDS) are enabled'
    resource_type = 'RDS'
    risk_level = 'Low'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, instances in kwargs['rds_lst'].items():
        for instance in instances:
            try:
                if len(instance['EnabledCloudwatchLogsExports']) <= 0:
                    result = False
                    failReason = "RDS logging is not enabled"
                    offenders.append(instance['DBInstanceIdentifier'])
            except KeyError:
                result = False
                failReason = "RDS logging is not enabled"
                offenders.append(instance['DBInstanceIdentifier'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# checks compliance for rds cluster deletion protection enabled
def rds_cluster_deletion_protection_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside rds :: rds_cluster_deletion_protection_enabled()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id5.13'
    compliance_type = 'Rds Cluster Deletion Protection Enabled'
    description = 'Checks if an Amazon Relational Database Service (Amazon RDS) cluster has deletion protection enabled'
    resource_type = 'RDS'
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, clusters in kwargs['cluster_list'].items():
        for cluster in clusters:
            if not cluster['DeletionProtection']:
                result = False
                failReason = "Deletion protection is not enabled"
                offenders.append(cluster['DBClusterIdentifier'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# checks compliance for rds cluster multi az enabled
def rds_cluster_multi_az_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside rds :: rds_cluster_multi_az_enabled()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id5.14'
    compliance_type = 'Rds Cluster Multi Az Enabled'
    description = 'Checks if an Amazon Relational Database Service (Amazon RDS) cluster has Multi-AZ replication ' \
                  'enabled'
    resource_type = 'RDS'
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, clusters in kwargs['cluster_list'].items():
        for cluster in clusters:
            if not cluster['MultiAZ']:
                result = False
                failReason = "MultiAZ is not enabled"
                offenders.append(cluster['DBClusterIdentifier'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# checks compliance for RdsInstanceIamAuthenticationEnabled
def rds_instance_iam_authentication_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside rds :: rds_instance_iam_authentication_enabled()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id5.15'
    compliance_type = 'Rds Instance Iam Authentication Enabled'
    description = "Checks if an Amazon Relational Database Service (Amazon RDS) instance has AWS Identity and Access " \
                  "Management (IAM) authentication enabled. The DB Engine should be one of 'mysql', 'postgres', " \
                  "'aurora', 'aurora-mysql', or 'aurora-postgresql'. The DB instance status should be one of " \
                  "'available', 'backing-up', 'storage-optimization', or 'storage-full'"
    resource_type = 'RDS'
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, instances in kwargs['rds_lst'].items():
        for instance in instances:
            if instance['Engine'] in ['mysql', 'postgres', 'aurora', 'aurora-mysql', 'aurora-postgresql']:
                if instance['DBInstanceStatus'] in ['available', 'backing-up', 'storage-optimization', 'storage-full']:
                    if not instance['IAMDatabaseAuthenticationEnabled']:
                        result = False
                        failReason = 'IAM Database Authentication is not enabled'
                        offenders.append(instance['DBInstanceIdentifier'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }
