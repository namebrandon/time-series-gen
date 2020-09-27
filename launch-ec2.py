# ## Most configuration items you will need start around line 35.
import boto3

# Read in secrets from file
# NEVER STORE SECRETS IN SOURCE CODE
# Before commiting to source validate secrets.txt is present in .gitignore!!
file = open("secrets.txt", "r")
key_id = file.readline().rstrip()
access_key = file.readline().rstrip()
file.close()

# userdata / first boot script which installs needed packages as well as ClickHouse
# you probably don't want to touch this unless you're sure

user_data_script = """#!/bin/bash
yum install -y curl epel-release mdadm nano python3 gcc gcc-c++ make python3-devel git screen
pip3 install --upgrade pip
curl -s "https://packagecloud.io/install/repositories/altinity/clickhouse-altinity-stable/script.rpm.sh" | bash
yum install -y clickhouse-server clickhouse-client
/etc/init.d/clickhouse-server restart
mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/nvme1n1 /dev/nvme2n1
sleep 6
mkfs.ext4 -F /dev/md0
mkdir /mnt/md0
mount /dev/md0 /mnt/md0
mdadm --verbose --detail --scan > /etc/mdadm.conf
echo '/dev/md0 /mnt/md0 ext4 defaults,nofail,discard 0 0' | sudo tee -a /etc/fstab
chown -R centos:centos /mnt/md0
mkdir /etc/clickhouse-server/conf.d
"""


# ##################################################################
# #############
# ### Configure your relevant information here

ec2_region = 'us-west-2'                # Change accordingly, but note that the AMI ID will change as a result
instance_type='c5ad.4xlarge'           # stick with the c5ad family or the userdata script may break
ami_id = 'ami-0a248ce88bcc7bd23'        # US-WEST-2 CentOS 7.5 X86_64
pem_key_name = 'brandon_west_2'         # the name of the pem key that already exists and that you wish to use
security_groups = ['uswest2_ssh_only']  # the NAME of your security group goes here, not SG ID

# ###
# #############
# ##################################################################

ec2 = boto3.resource('ec2', region_name=ec2_region ,aws_access_key_id=key_id,aws_secret_access_key=access_key)
instances = ec2.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
    KeyName=pem_key_name,
    SecurityGroups=security_groups,
    UserData=user_data_script)
instance = instances[0]

# Wait for the instance to enter the running state
instance.wait_until_running()

# Reload the instance attributes
instance.load()

print(instance.public_ip_address)
print(instance.id)
