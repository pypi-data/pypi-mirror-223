"""
Contains the methods to check compliance for ec2
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks the compliance ec2 instance no public Ip
def ec2_instance_no_public_ip(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_instance_no_public_ip()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.32'
    compliance_type = 'Ec2 Instance No Public Ip'
    description = 'Checks whether Amazon Elastic Compute Cloud (Amazon EC2) instances have a public IP association. ' \
                  'The rule is NON_COMPLIANT if the publicIp field is present in the Amazon EC2 instance ' \
                  'configuration item'
    resource_type = 'EC2'
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

    for region, reservations in kwargs['instances'].items():
        for reservation in reservations:
            for instance in reservation['Instances']:
                try:
                    public_ip = instance['PublicIpAddress']
                    if not public_ip == '':
                        result = False
                        failReason = 'Public Ip is assigned to the instance'
                        offenders.append(instance['InstanceId'])
                except KeyError:
                    pass

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