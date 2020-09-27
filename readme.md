# Synthetic Time-Series Testing with ClickHouse 

Many synthetic time-series datasets are based on uniform or normal random number generation that creates data that is independent and identically distributed. This is not necessarily a characteristic that is found in many time series datasets. The goal of this code is to provide the capability to generate time series datasets based on an autoregressive component that can be further customized as needed. 

The code as shared here is configured to do the following:

* Generate 2.5 billion rows of true auto-regressive time-series data based on stochastic processes with white noise. 

* Instantiating a ClickHouse environment running CentOS 7.5 to query the data.

## Notes

AWS is used for this effort, you will need an account and if you run the code as is, **you will incur costs of at least $25 USD and potentially more if you aren't careful**. 

You will need an existing AWS account, a default VPC with internet access, a functional security group that allows 22/TCP inbound and all outbound traffic, an ec2 .pem key, an IAM role with the rights to launch an ec2 instance and the associated secret / account key. The default region for this code is us-west-2. Please note that there are also many account specific items such as security group names, .pem key name, etc.. you will need to update this for your account / configuration.


```
---\
---\ create-db.sql - SQL DDL to create ClickHouse database and table
---\ gen.py - Python 3 script that is configurable. Data size and details are set here.
---\ launch-ec2.py - Python 3 script that uses AWS SDK to instantiate data generation and query environment
---\ load-data.sh - bash script to load data to ClickHouse
---\ requirements.txt - pip requirements
---\ secrets.txt - you create this. Two lines, account key on first, secret on second line.

```

## Usage
*Important* - The user data script in launch-ec2.py will assume you have two local NVME disks and will create an RAID 0 array. Unless you know how to configure this for your instance types, it is suggested you stay within the c5ad family of ec2 instance types. 

### Data Generation Stage
1. Clone the repo
2. Create secrets.txt with your relevant account in the root of the repo
3. Update launch-ec2.py with your relevant information (there are account / region specific settings, this will not work out of the box.
4. execute the launch-ec2.py script and capture the output IP address of the ec2 instance.
5. ssh into the instance (note that the user will be "centos" unless a different AMI was chosen.
6. cd to /mnt/md0 and clone this repo once more (note that it may take 10+ minutes for the userdata script to fully execute. Please wait for md0 to apepar.)
7. install all pip requirements / pip3 install -r requirements.txt
8. using nano or another editor, make any changes needed to gen.py
9. Launch a screen session (optional, but suggested) and execute gen.py ( python3 gen.py ) and wait. Data is in data/ in .csv format.

### Data Import
1. chmod +x create-db.sh and load-data.sh
2. launch the ClickHouse client to validate the install (clickhouse-client). Assuming you were launched into the SQL client, "exit" back to the shell prompt. 
3. ./create-db.sh
4. Launch a screen session (again, optional but suggested), and ./load-data.sh
5. Wait

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

