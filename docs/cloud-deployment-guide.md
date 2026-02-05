# Aya 23 Cloud Deployment Guide

## Step-by-Step Instructions for Google Cloud, AWS, and Azure

> **Version:** 1.0  
> **Date:** February 2026  
> **Target Audience:** Developers, DevOps, IT Administrators  
> **Difficulty:** Beginner to Intermediate

---

## Table of Contents

-   1\. Overview & Prerequisites

-   2\. Quick Start (Recommended for Beginners)

-   3\. Google Cloud Platform (GCP) Deployment

-   4\. Amazon Web Services (AWS) Deployment

-   5\. Microsoft Azure Deployment

-   6\. Post-Deployment Setup

-   7\. Monitoring & Maintenance

-   8\. Cost Optimization

-   9\. Troubleshooting

-   10\. Security Best Practices

# 1. Overview & Prerequisites

This guide walks you through deploying Aya 23 (8B parameter model) on cloud infrastructure. Cloud deployment is ideal for the proof-of-concept phase as it requires no hardware investment and can be set up in under an hour.

## 1.1 Why Start with Cloud?

-   No upfront hardware costs (pay only for usage)

-   Quick setup (\< 1 hour to deploy)

-   Easy to scale and experiment

-   Free credits available (GCP: \$300, AWS: \$100-300, Azure: \$200)

-   Test before committing to on-premises hardware

## 1.2 Prerequisites

Before starting, ensure you have:

-   A credit card (required for account verification, even with free credits)

-   Basic command line familiarity

-   SSH client installed (comes with macOS/Linux, use PuTTY on Windows)

-   GitHub account (to clone the repository)

## 1.3 Expected Costs

  --------------------------------------------------------------------------
  Cloud Provider          GPU Instance Type       Cost/Hour (USD)
  ----------------------- ----------------------- --------------------------
  Google Cloud            n1-standard-4 + T4      \$0.35 + \$0.35 = \$0.70

  AWS                     g4dn.xlarge             \$0.526

  Azure                   NC6s_v3                 \$0.90

                          Monthly (24/7)          \~\$500-650/month
  --------------------------------------------------------------------------

**⚠️ NOTE: Start with free credits! All providers offer \$100-\$300 in free credits for new accounts.**

# 2. Quick Start (Recommended for Beginners)

This is the fastest path to get Aya 23 running. We recommend Google Cloud for beginners due to its generous \$300 free credit and straightforward setup.

## Step 1: Sign up for Google Cloud

-   Go to https://cloud.google.com/free

-   Click \"Get started for free\"

-   Sign in with your Google account

-   Enter credit card details (won\'t be charged during free trial)

-   Receive \$300 in free credits (valid for 90 days)

## Step 2: Create a GPU VM Instance

Open Google Cloud Console and run this command in Cloud Shell:

gcloud compute instances create aya-23-instance \\\
\--zone=us-central1-a \\\
\--machine-type=n1-standard-4 \\\
\--accelerator=type=nvidia-tesla-t4,count=1 \\\
\--image-family=ubuntu-2204-lts \\\
\--image-project=ubuntu-os-cloud \\\
\--boot-disk-size=100GB \\\
\--boot-disk-type=pd-standard \\\
\--maintenance-policy=TERMINATE \\\
\--metadata=startup-script=\'#!/bin/bash\
apt-get update\
apt-get install -y python3-pip git\
\'

**⚠️ This takes 2-3 minutes. The VM will be created with Ubuntu 22.04 and 100GB disk.**

## Step 3: Install GPU Drivers

SSH into your instance:

gcloud compute ssh aya-23-instance \--zone=us-central1-a

Install NVIDIA drivers:

curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py \--output install_gpu_driver.py\
sudo python3 install_gpu_driver.py

Verify GPU is working:

nvidia-smi

You should see output showing your T4 GPU.

## Step 4: Clone and Setup SA Edu LLM

\# Clone the repository\
git clone https://github.com/\[your-org\]/sa-edu-llm.git\
cd sa-edu-llm\
\
\# Create virtual environment\
python3 -m venv venv\
source venv/bin/activate\
\
\# Install dependencies\
pip install -r requirements.txt

## Step 5: Download Aya 23 Model

\# This downloads \~16GB, takes 10-15 minutes\
python scripts/download_model.py \--quantization int8\
\
\# The int8 quantization reduces VRAM usage by 50%\
\# Perfect for T4 GPU (16GB VRAM)

## Step 6: Start the Server

\# Create .env file\
cat \> .env \<\< EOF\
MODEL_PATH=./models/base/aya-23-8b\
MAX_TOKENS=2048\
TEMPERATURE=0.7\
LOG_LEVEL=INFO\
API_PORT=8000\
EOF\
\
\# Run the server\
python scripts/run_server.py

## Step 7: Access from Your Computer

In a new terminal on your local machine:

\# Create SSH tunnel\
gcloud compute ssh aya-23-instance \\\
\--zone=us-central1-a \\\
\-- -L 8000:localhost:8000

Now open your browser and go to: http://localhost:8000

**⚠️ ✅ SUCCESS! You now have Aya 23 running in the cloud. Test it with a simple question like \"What is photosynthesis?\"**

# 3. Google Cloud Platform (GCP) - Detailed Guide

## 3.1 Account Setup

Complete account setup with free credits:

-   Visit https://cloud.google.com/free

-   Sign up with Google account

-   Enter credit card (required but not charged)

-   Activate \$300 free credit (90-day validity)

-   Create a project (e.g., \"sa-edu-llm\")

## 3.2 Enable Required APIs

\# Enable Compute Engine API\
gcloud services enable compute.googleapis.com\
\
\# Enable Cloud Storage (for model caching)\
gcloud services enable storage-api.googleapis.com

## 3.3 Increase GPU Quota (Important!)

By default, new accounts have 0 GPU quota. You must request an increase:

-   Go to: Console → IAM & Admin → Quotas

-   Filter by: \"NVIDIA T4 GPUs\"

-   Select: \"NVIDIA T4 GPUs\" in your preferred region (us-central1)

-   Click \"EDIT QUOTAS\"

-   Request limit: 1 (sufficient for proof of concept)

-   Provide justification: \"Educational AI project for South African schools\"

**⚠️ Quota increase typically approved within 24-48 hours. Apply early!**

## 3.4 Choose the Right GPU

  -------------------------------------------------------------------------------
  GPU Type          VRAM              Best For                  Cost/Hour
  ----------------- ----------------- ------------------------- -----------------
  T4                16GB              Proof of concept (INT8)   \$0.35

  L4                24GB              Production (FP16)         \$0.70

  V100              16GB              Fast inference            \$2.48

  A100              40GB              Multiple users            \$3.67
  -------------------------------------------------------------------------------

✅ Recommendation: Start with T4 for proof of concept.

## 3.5 Create Instance with Optimal Configuration

gcloud compute instances create aya-23-prod \\\
\--project=sa-edu-llm \\\
\--zone=us-central1-a \\\
\--machine-type=n1-standard-4 \\\
\--accelerator=type=nvidia-tesla-t4,count=1 \\\
\--image-family=ubuntu-2204-lts \\\
\--image-project=ubuntu-os-cloud \\\
\--boot-disk-size=100GB \\\
\--boot-disk-type=pd-ssd \\\
\--maintenance-policy=TERMINATE \\\
\--provisioning-model=STANDARD \\\
\--scopes=https://www.googleapis.com/auth/cloud-platform \\\
\--tags=http-server,https-server \\\
\--metadata=startup-script=\'#!/bin/bash\
\# Install basic dependencies\
apt-get update\
apt-get install -y python3-pip python3-venv git curl\
\
\# Install Docker (optional)\
curl -fsSL https://get.docker.com -o get-docker.sh\
sh get-docker.sh\
\
\# Create app user\
useradd -m -s /bin/bash llmuser\
\'

## 3.6 Set Up Firewall Rules

\# Allow HTTP/HTTPS traffic\
gcloud compute firewall-rules create allow-http-https \\\
\--allow tcp:80,tcp:443,tcp:8000 \\\
\--source-ranges 0.0.0.0/0 \\\
\--target-tags http-server\
\
\# For security, restrict to your IP:\
\# Replace YOUR_IP with your actual IP\
gcloud compute firewall-rules create allow-http-https \\\
\--allow tcp:8000 \\\
\--source-ranges YOUR_IP/32 \\\
\--target-tags http-server

**⚠️ SECURITY: Never expose the API to 0.0.0.0/0 in production. Use VPN or IP whitelisting.**

## 3.7 Install and Configure

SSH into instance:

gcloud compute ssh aya-23-prod \--zone=us-central1-a

Install GPU drivers and dependencies:

\# Install GPU drivers\
curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py \--output install_gpu_driver.py\
sudo python3 install_gpu_driver.py\
\
\# Verify\
nvidia-smi\
\
\# Install CUDA toolkit\
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb\
sudo dpkg -i cuda-keyring_1.1-1_all.deb\
sudo apt-get update\
sudo apt-get -y install cuda-toolkit-12-1\
\
\# Set up environment\
echo \'export PATH=/usr/local/cuda-12.1/bin:\$PATH\' \>\> \~/.bashrc\
echo \'export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:\$LD_LIBRARY_PATH\' \>\> \~/.bashrc\
source \~/.bashrc

# 4. Amazon Web Services (AWS) - Detailed Guide

## 4.1 Account Setup

-   Visit https://aws.amazon.com/free

-   Create new AWS account

-   Complete identity verification

-   Note: Free tier includes 750 hours of t2.micro (CPU only)

-   GPU instances are NOT in free tier but some credits available

## 4.2 Request GPU Instance Quota

AWS requires quota increase for GPU instances:

-   Go to: Service Quotas → Amazon EC2

-   Search for: \"Running On-Demand G and VT instances\"

-   Request increase to: 4 vCPUs (for g4dn.xlarge)

-   Justification: \"Educational AI deployment for South African schools\"

-   Approval time: Usually 24-48 hours

## 4.3 Launch EC2 Instance

Using AWS Console:

-   Go to EC2 Dashboard → Launch Instance

-   Name: \"aya-23-instance\"

-   AMI: Deep Learning AMI (Ubuntu 22.04)

-   Instance type: g4dn.xlarge

-   Key pair: Create new (download .pem file)

-   Storage: 100 GB gp3

-   Security group: Allow SSH (22), HTTP (80), Custom TCP (8000)

## 4.4 Connect to Instance

\# Make key file read-only\
chmod 400 your-key.pem\
\
\# SSH into instance\
ssh -i your-key.pem ubuntu@YOUR_INSTANCE_PUBLIC_IP

## 4.5 Verify GPU and Setup

\# Check GPU\
nvidia-smi\
\
\# The Deep Learning AMI comes with drivers pre-installed\
\# Activate pre-configured environment\
source activate pytorch\
\
\# Clone and setup\
git clone https://github.com/\[your-org\]/sa-edu-llm.git\
cd sa-edu-llm\
pip install -r requirements.txt

## 4.6 Configure Auto-Start on Reboot

\# Create systemd service\
sudo tee /etc/systemd/system/aya-llm.service \> /dev/null \<\< EOF\
\[Unit\]\
Description=Aya 23 LLM Service\
After=network.target\
\
\[Service\]\
Type=simple\
User=ubuntu\
WorkingDirectory=/home/ubuntu/sa-edu-llm\
Environment=\"PATH=/home/ubuntu/sa-edu-llm/venv/bin\"\
ExecStart=/home/ubuntu/sa-edu-llm/venv/bin/python scripts/run_server.py\
Restart=always\
\
\[Install\]\
WantedBy=multi-user.target\
EOF\
\
\# Enable and start\
sudo systemctl enable aya-llm\
sudo systemctl start aya-llm\
\
\# Check status\
sudo systemctl status aya-llm

# 5. Microsoft Azure - Detailed Guide

## 5.1 Account Setup

-   Visit https://azure.microsoft.com/free

-   Create free account with \$200 credit (30 days)

-   Requires credit card verification

## 5.2 Install Azure CLI

\# On Ubuntu/Debian\
curl -sL https://aka.ms/InstallAzureCLIDeb \| sudo bash\
\
\# On macOS\
brew install azure-cli\
\
\# On Windows\
\# Download from: https://aka.ms/installazurecliwindows\
\
\# Login\
az login

## 5.3 Create Resource Group

\# Create resource group in South Africa North region\
az group create \\\
\--name sa-edu-llm-rg \\\
\--location southafricanorth

**⚠️ southafricanorth region is physically located in South Africa - lower latency for SA users!**

## 5.4 Create VM with GPU

az vm create \\\
\--resource-group sa-edu-llm-rg \\\
\--name aya-23-vm \\\
\--image Ubuntu2204 \\\
\--size Standard_NC6s_v3 \\\
\--admin-username azureuser \\\
\--generate-ssh-keys \\\
\--public-ip-sku Standard \\\
\--storage-sku Premium_LRS \\\
\--os-disk-size-gb 128

## 5.5 Open Ports

az vm open-port \\\
\--resource-group sa-edu-llm-rg \\\
\--name aya-23-vm \\\
\--port 8000 \\\
\--priority 1001

## 5.6 Connect and Setup

\# Get public IP\
az vm show \\\
\--resource-group sa-edu-llm-rg \\\
\--name aya-23-vm \\\
\--show-details \\\
\--query publicIps \\\
\--output tsv\
\
\# SSH\
ssh azureuser@YOUR_PUBLIC_IP

# 6. Post-Deployment Setup (All Providers)

## 6.1 Install Monitoring

\# Install Prometheus node exporter\
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz\
tar xvfz node_exporter-1.7.0.linux-amd64.tar.gz\
sudo cp node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/\
sudo useradd -rs /bin/false node_exporter\
\
\# Create systemd service\
sudo tee /etc/systemd/system/node_exporter.service \> /dev/null \<\< EOF\
\[Unit\]\
Description=Node Exporter\
After=network.target\
\
\[Service\]\
User=node_exporter\
Group=node_exporter\
Type=simple\
ExecStart=/usr/local/bin/node_exporter\
\
\[Install\]\
WantedBy=multi-user.target\
EOF\
\
sudo systemctl daemon-reload\
sudo systemctl start node_exporter\
sudo systemctl enable node_exporter

## 6.2 Set Up Automatic Backups

Create daily backup script:

\# Create backup script\
cat \> \~/backup.sh \<\< \'EOF\'\
#!/bin/bash\
TIMESTAMP=\$(date +%Y%m%d\_%H%M%S)\
BACKUP_DIR=\~/backups/\$TIMESTAMP\
\
mkdir -p \$BACKUP_DIR\
\
\# Backup logs\
cp -r \~/sa-edu-llm/logs \$BACKUP_DIR/\
\
\# Backup config\
cp \~/sa-edu-llm/.env \$BACKUP_DIR/\
\
\# Backup any fine-tuned models\
if \[ -d \~/sa-edu-llm/models/fine-tuned \]; then\
cp -r \~/sa-edu-llm/models/fine-tuned \$BACKUP_DIR/\
fi\
\
\# Keep only last 7 days\
find \~/backups -type d -mtime +7 -exec rm -rf {} +\
\
echo \"Backup completed: \$BACKUP_DIR\"\
EOF\
\
chmod +x \~/backup.sh\
\
\# Add to crontab (daily at 2 AM)\
(crontab -l 2\>/dev/null; echo \"0 2 \* \* \* \~/backup.sh\") \| crontab -

## 6.3 Configure Log Rotation

sudo tee /etc/logrotate.d/aya-llm \> /dev/null \<\< EOF\
/home/\*/sa-edu-llm/logs/\*.log {\
daily\
missingok\
rotate 14\
compress\
delaycompress\
notifempty\
create 0640 \$USER \$USER\
}\
EOF

# 7. Monitoring & Maintenance

## 7.1 Check System Health

\# GPU usage\
nvidia-smi\
\
\# Disk space\
df -h\
\
\# Memory usage\
free -h\
\
\# Service status\
sudo systemctl status aya-llm\
\
\# View logs\
tail -f \~/sa-edu-llm/logs/app.log

## 7.2 Set Up Alerts

Create simple monitoring script:

cat \> \~/monitor.sh \<\< \'EOF\'\
#!/bin/bash\
\
\# Check if service is running\
if ! systemctl is-active \--quiet aya-llm; then\
echo \"ALERT: Aya LLM service is down!\" \| mail -s \"Service Down\" your@email.com\
sudo systemctl start aya-llm\
fi\
\
\# Check disk space\
DISK_USAGE=\$(df -h / \| awk \'NR==2 {print \$5}\' \| sed \'s/%//\')\
if \[ \$DISK_USAGE -gt 80 \]; then\
echo \"ALERT: Disk usage is \${DISK_USAGE}%\" \| mail -s \"Disk Space Warning\" your@email.com\
fi\
\
\# Check GPU temperature\
GPU_TEMP=\$(nvidia-smi \--query-gpu=temperature.gpu \--format=csv,noheader)\
if \[ \$GPU_TEMP -gt 80 \]; then\
echo \"ALERT: GPU temperature is \${GPU_TEMP}°C\" \| mail -s \"GPU Overheat Warning\" your@email.com\
fi\
EOF\
\
chmod +x \~/monitor.sh\
\
\# Run every 5 minutes\
(crontab -l 2\>/dev/null; echo \"\*/5 \* \* \* \* \~/monitor.sh\") \| crontab -

# 8. Cost Optimization Strategies

## 8.1 Use Preemptible/Spot Instances

Save up to 70% using preemptible instances:

Google Cloud:

gcloud compute instances create aya-23-spot \\\
\--preemptible \\\
\--zone=us-central1-a \\\
\--machine-type=n1-standard-4 \\\
\--accelerator=type=nvidia-tesla-t4,count=1 \\\
\--image-family=ubuntu-2204-lts \\\
\--image-project=ubuntu-os-cloud \\\
\--boot-disk-size=100GB

**⚠️ Preemptible instances can be terminated at any time. Only use for development/testing, not production.**

## 8.2 Auto-Stop During Off Hours

Automatically stop instance at night to save costs:

\# Stop at 6 PM weekdays\
0 18 \* \* 1-5 gcloud compute instances stop aya-23-instance \--zone=us-central1-a\
\
\# Start at 7 AM weekdays\
0 7 \* \* 1-5 gcloud compute instances start aya-23-instance \--zone=us-central1-a

## 8.3 Use Committed Use Discounts

For production deployments, commit to 1-3 years for 37-55% discount:

-   GCP: Committed use contracts (37-55% discount)

-   AWS: Reserved Instances (40-60% discount)

-   Azure: Reserved VM Instances (up to 72% discount)

# 9. Common Issues & Troubleshooting

## 9.1 GPU Not Detected

Problem: nvidia-smi shows no GPU

Solution:

\# Reinstall drivers\
sudo apt-get purge nvidia-\*\
sudo apt-get update\
sudo apt-get install -y ubuntu-drivers-common\
sudo ubuntu-drivers autoinstall\
sudo reboot

## 9.2 Out of Memory Errors

Problem: CUDA out of memory

Solutions:

-   Use INT8 quantization: \--quantization int8

-   Reduce max_tokens in .env

-   Reduce batch_size for inference

-   Upgrade to larger GPU (L4 or A100)

## 9.3 Slow Model Loading

Problem: Model takes 5+ minutes to load

Solutions:

-   Use SSD instead of HDD

-   Enable model caching: export TRANSFORMERS_CACHE=/fast/storage

-   Use INT8 quantization (smaller model size)

## 9.4 Connection Refused

Problem: Cannot connect to port 8000

Solutions:

\# Check if service is running\
sudo systemctl status aya-llm\
\
\# Check firewall\
sudo ufw status\
\
\# Check if port is open\
sudo netstat -tulpn \| grep 8000\
\
\# Check logs\
tail -f \~/sa-edu-llm/logs/app.log

# 10. Security Best Practices

## 10.1 SSH Key Security

-   Never use password authentication (use SSH keys only)

-   Keep private keys secure and never commit to git

-   Use different keys for different environments

-   Rotate keys every 6 months

## 10.2 Network Security

\# Enable UFW firewall\
sudo ufw default deny incoming\
sudo ufw default allow outgoing\
sudo ufw allow ssh\
sudo ufw allow 8000/tcp\
sudo ufw enable\
\
\# Limit SSH attempts\
sudo ufw limit ssh

## 10.3 Regular Updates

\# Create update script\
cat \> \~/update.sh \<\< \'EOF\'\
#!/bin/bash\
sudo apt-get update\
sudo apt-get upgrade -y\
sudo apt-get autoremove -y\
sudo apt-get autoclean\
EOF\
\
chmod +x \~/update.sh\
\
\# Run weekly\
(crontab -l 2\>/dev/null; echo \"0 3 \* \* 0 \~/update.sh\") \| crontab -

## 10.4 Enable HTTPS

For production, always use HTTPS:

\# Install Certbot\
sudo snap install \--classic certbot\
\
\# Get certificate (requires domain name)\
sudo certbot \--nginx -d yourdomain.com\
\
\# Auto-renewal is configured automatically

# Appendix A: Quick Reference Commands

## Google Cloud

\# List instances\
gcloud compute instances list\
\
\# Start instance\
gcloud compute instances start INSTANCE_NAME \--zone=ZONE\
\
\# Stop instance\
gcloud compute instances stop INSTANCE_NAME \--zone=ZONE\
\
\# Delete instance\
gcloud compute instances delete INSTANCE_NAME \--zone=ZONE\
\
\# SSH\
gcloud compute ssh INSTANCE_NAME \--zone=ZONE

## AWS

\# List instances\
aws ec2 describe-instances \--query \'Reservations\[\*\].Instances\[\*\].\[InstanceId,State.Name,PublicIpAddress\]\'\
\
\# Start instance\
aws ec2 start-instances \--instance-ids INSTANCE_ID\
\
\# Stop instance\
aws ec2 stop-instances \--instance-ids INSTANCE_ID\
\
\# Terminate instance\
aws ec2 terminate-instances \--instance-ids INSTANCE_ID

## Azure

\# List VMs\
az vm list \--resource-group RESOURCE_GROUP \--output table\
\
\# Start VM\
az vm start \--resource-group RESOURCE_GROUP \--name VM_NAME\
\
\# Stop VM (deallocate to stop billing)\
az vm deallocate \--resource-group RESOURCE_GROUP \--name VM_NAME\
\
\# Delete VM\
az vm delete \--resource-group RESOURCE_GROUP \--name VM_NAME

ffline capability.

For support, refer to:

-   GitHub Issues: https://github.com/\[your-org\]/sa-edu-llm/issues


-   Email: llm-support@ncpd.org.za
