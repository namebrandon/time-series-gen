# Synthetic Big Data Time Series Testing with ClickHouse 

Many synthetic time series datasets are based on uniform or normal random number generation that creates data that is independent and identically distributed. This is not necessarily a characteristic that is found in many time series datasets. The goal of this code is to provide the capability to generate very large time series datasets based on an autoregressive component (as to establish temporal dependencies) and that that can be further customized as needed. 

The code as shared here is configured to do the following:

* Generate 2.5 billion rows of true auto-regressive time-series data a gaussian / white noise based error process. 

* Instantiate an AWS-based ClickHouse environment running CentOS 7.5 to query the data.

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
---\ time-series.conf - ClickHouse conf.d override for storage - points to nvme raid 0 array

```

## Usage
*Important* - The user data script in launch-ec2.py will assume you have two local NVME disks and will create an RAID 0 array. Unless you know how to configure this for your instance types, it is suggested you stay within the c5ad family of ec2 instance types. 

### Prerequisites
* An environment is needed to launch the EC2 instance we'll be using for most of this effort. This environment needs Python 3 (this was built / tested with 3.6) and an equivalent pip (check with python3 --version and pip3 --version or pip-3.6 --version). Getting to this point is beyond the scope of the readme, please check with your favorite search enginge on installing Python / pip 3 for your platform.
### Data Generation Stage
1. Clone the repo ```git clone https://github.com/namebrandon/time-series-gen.git```
2. The only import we need is boto3 for now. You can pip install the requirements.txt which is overkill for this stage, or just pip install boto3. Ensure you are using pip for Python 3 and are targeting your python 3 environment. For me, this required the following ``` pip3 install --upgrade pip && pip3 install boto3 ```
2. Create secrets.txt with your relevant account in the root of the repo. 2 lines only, first line is your account key, the second line is your secret.
3. Update launch-ec2.py with your relevant information (there are account / region specific settings, this will not work out of the box.
4. Execute the launch-ec2.py script and capture the output IP address of the ec2 instance. ```python3 launch-ec2.py```
5. ssh into the instance (note that the user will be "centos" unless a different AMI was chosen.) ``` ssh -i path-to-pem-file/your.pem centos@your-instance-ip```
6. cd to /mnt/md0 and clone this repo once more (__note__: it may take 10+ minutes for the userdata script to fully execute. Please wait for md0 to appear.) ```git clone https://github.com/namebrandon/time-series-gen.git```
7. Install all pip requirements / ```cd time-series-gen/ && pip3 install -r requirements.txt```
8. Using nano or another editor, make any changes needed to gen.py (by default it will generate 2.5 billion rows of data using 96 cores. This will take ~6 hours)
9. Launch a screen session (optional, but suggested) and execute gen.py and wait. Data is in data/ in .csv format. ```screen -dm bash -c 'python3 gen.py; exec sh'``` (For those of you unfamiliar with screen, ```screen -r``` will reattach you to that session, and once in the session, CTRL+A D will disconnect you. If you have multiple screen sessions, ```screen -list``` will enumerate them all.)


### Data Import
1. From the repo root directory ```chmod +x *.sh```
2. Copy the config override to point ClickHouse storage to raid 0 array / ```sudo cp time-series.conf /etc/clickhouse-server/conf.d/```
3. Restart ClickHouse server - ```sudo service clickhouse-server restart```
You should see a message about a new ClickHouse data directory being created.
4. Launch the ClickHouse client to validate the install ( ```clickhouse-client ```). Assuming you were launched into the SQL client, "exit" back to the shell prompt. 
5. `````./create-db.sh`````
6. Launch a screen session (again, optional but suggested)
7. `````screen -dm bash -c './load-data.sh; exec sh'`````
5. Wait for loading to complete. Loading is relatively quick, it should take less than 35 minutes for all 2.5 billion rows to load.

### Query
1. From your bash prompt - ```clickhouse-client```
2. Validate data is present ```SELECT COUNT(*) FROM perftest.exchange_data;```

## Contributing / Issues
For issues, please open a GitHub issue with as much detail as you can provide. I'll support this as best I can, but I make no promises. Please don't email me directly.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Citations

*Synthetic Time Series - J. R. Maat, A. Malali, and P. Protopapas, “TimeSynth: A Multipurpose Library for Synthetic Time Series in Python,” 2017. [Online].*
Available: http://github.com/TimeSynth/TimeSynth