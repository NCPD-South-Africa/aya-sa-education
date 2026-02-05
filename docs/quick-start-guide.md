# 🚀 Aya 23 Cloud Deployment - Quick Start Guide

## Choose Your Path

### 🟢 Path 1: Absolute Beginner (Recommended)
**Time: 30 minutes | Cost: FREE (with $300 credits)**

```
┌─────────────────────────────────────────┐
│  1. Sign up for Google Cloud           │
│     → Get $300 free credits             │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  2. Run ONE command in Cloud Shell     │
│     (Copy-paste from this guide)        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  3. Wait 10 minutes (automatic setup)   │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  4. Access Aya 23 in your browser!      │
└─────────────────────────────────────────┘
```

### 🟡 Path 2: Developer
**Time: 1-2 hours | Cost: ~$0.70/hour**

Use the automated script provided in this folder.

### 🔴 Path 3: Advanced
**Time: 2-4 hours | Full control**

Follow the detailed 50+ page guide for custom configuration.

---

## 🟢 BEGINNER PATH: Step-by-Step

### Step 1: Sign Up for Google Cloud (5 minutes)

1. Go to: https://cloud.google.com/free
2. Click **"Get started for free"**
3. Sign in with your Google account
4. Enter credit card details ⚠️ *You won't be charged - this is just for verification*
5. Agree to terms and complete signup

✅ **You now have $300 in free credits valid for 90 days!**

---

### Step 2: Request GPU Quota (2 minutes + 24-48 hour wait)

⚠️ **IMPORTANT: Do this first! Approval takes 24-48 hours.**

1. In Google Cloud Console, go to: **☰ Menu → IAM & Admin → Quotas**
2. In the filter box, type: `NVIDIA T4 GPUs`
3. Check the box next to **"NVIDIA T4 GPUs"** for region `us-central1`
4. Click **"EDIT QUOTAS"** at the top
5. In the "New limit" field, enter: `1`
6. In "Request description", write:
   ```
   Educational AI project for South African schools - deploying Aya 23 
   multilingual model for curriculum-aligned tutoring. Proof of concept 
   phase, requiring 1 GPU for initial testing with 2-3 pilot schools.
   ```
7. Click **"SUBMIT REQUEST"**

📧 You'll receive an email when approved (usually 24-48 hours).

**While waiting, continue with the next steps to prepare.**

---

### Step 3: Create Your Project (2 minutes)

1. In Cloud Console, click the **project dropdown** at the top
2. Click **"NEW PROJECT"**
3. Project name: `sa-edu-llm`
4. Click **"CREATE"**
5. Wait a few seconds for the project to be created
6. Select your new project from the dropdown

---

### Step 4: Deploy Aya 23 (1 command!)

Once your GPU quota is approved:

1. Click the **Activate Cloud Shell** button (>_ icon) at the top right
2. Copy and paste this ENTIRE command:

```bash
# This one command does everything!
gcloud compute instances create aya-23-instance \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=100GB \
  --boot-disk-type=pd-ssd \
  --maintenance-policy=TERMINATE \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y python3-pip python3-venv git curl
    
    # Install GPU drivers
    curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py -o /tmp/install_gpu_driver.py
    python3 /tmp/install_gpu_driver.py
  '
```

3. Press **Enter**
4. Type `y` and press Enter to confirm
5. Wait 3-5 minutes for the VM to be created

✅ **Your cloud server is now running!**

---

### Step 5: Set Up Aya 23 (10 minutes)

1. In Cloud Shell, SSH into your instance:
```bash
gcloud compute ssh aya-23-instance --zone=us-central1-a
```

2. Verify GPU is working:
```bash
nvidia-smi
```
You should see your T4 GPU listed. ✅

3. Clone the SA Edu LLM repository:
```bash
git clone https://github.com/your-org/sa-edu-llm.git
cd sa-edu-llm
```

4. Set up Python environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Download Aya 23 model (this takes 10-15 minutes):
```bash
python scripts/download_model.py --quantization int8
```

☕ **Grab a coffee while the model downloads (~16GB)**

6. Create configuration file:
```bash
cat > .env << EOF
MODEL_PATH=./models/base/aya-23-8b
MAX_TOKENS=2048
TEMPERATURE=0.7
LOG_LEVEL=INFO
API_PORT=8000
EOF
```

7. Start the server:
```bash
python scripts/run_server.py
```

You should see:
```
🚀 Starting Aya 23 Server
✓ Model loaded successfully
✓ Server running on http://0.0.0.0:8000
```

✅ **Aya 23 is now running!**

---

### Step 6: Access from Your Computer

**Option A: SSH Tunnel (Recommended for testing)**

1. Open a NEW terminal on your local computer
2. Run:
```bash
gcloud compute ssh aya-23-instance --zone=us-central1-a -- -L 8000:localhost:8000
```
3. Open your browser and go to: http://localhost:8000
4. Try asking: "What is photosynthesis?"

**Option B: Public Access (For sharing with teachers)**

1. Create firewall rule:
```bash
gcloud compute firewall-rules create allow-aya-llm \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server
```

2. Get your public IP:
```bash
gcloud compute instances describe aya-23-instance --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

3. Access at: http://YOUR_IP_ADDRESS:8000

⚠️ **WARNING: This exposes your API to the internet. Only use for testing!**

---

## 💰 Managing Costs

### Your current setup costs:
- **GPU (T4)**: $0.35/hour
- **VM (n1-standard-4)**: $0.19/hour
- **Storage (100GB SSD)**: $0.17/day
- **Total**: ~$0.70/hour = ~$500/month if running 24/7

### 💡 Save Money:

**1. Stop when not in use:**
```bash
# Stop the instance (you stop paying for compute, only pay for storage)
gcloud compute instances stop aya-23-instance --zone=us-central1-a

# Start when needed
gcloud compute instances start aya-23-instance --zone=us-central1-a
```

**2. Auto-stop at night:**
```bash
# Stop at 6 PM
0 18 * * * gcloud compute instances stop aya-23-instance --zone=us-central1-a

# Start at 8 AM
0 8 * * * gcloud compute instances start aya-23-instance --zone=us-central1-a
```

**3. Use your free credits wisely:**
- $300 credits = ~430 hours of runtime
- Running 8 hours/day = ~50 days
- Running 24/7 = ~18 days

---

## ✅ Checklist

- [ ] Google Cloud account created
- [ ] GPU quota requested and approved
- [ ] Project created (`sa-edu-llm`)
- [ ] VM instance created
- [ ] GPU verified with `nvidia-smi`
- [ ] Aya 23 model downloaded
- [ ] Server running
- [ ] Able to access and test queries
- [ ] Cost monitoring set up

---

## 🆘 Common Issues

### Issue: "Quota exceeded" error when creating instance
**Solution:** Your GPU quota request hasn't been approved yet. Wait for approval email.

### Issue: `nvidia-smi` shows "command not found"
**Solution:** Drivers not installed. Run:
```bash
curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py -o install_gpu_driver.py
sudo python3 install_gpu_driver.py
```

### Issue: Model download fails
**Solution:** Check internet connection and disk space:
```bash
df -h  # Check disk space (need ~20GB free)
```

### Issue: Server won't start - "CUDA out of memory"
**Solution:** Make sure you used `--quantization int8` when downloading.

### Issue: Can't access from browser
**Solution:** 
1. Check server is running: `ps aux | grep python`
2. Check firewall: `gcloud compute firewall-rules list`
3. Use SSH tunnel instead of public IP

---

## 📚 Next Steps

Once you have Aya 23 running:

1. **Test with curriculum questions**
   - Try math problems from CAPS curriculum
   - Test science explanations
   - Try questions in isiZulu or Afrikaans

2. **Share with 2-3 teachers**
   - Get their feedback on accuracy
   - Note any inappropriate responses
   - Collect suggestions for improvement

3. **Monitor usage**
   - Track costs in GCP Console
   - Note response times
   - Identify most-asked topics

4. **Plan next phase**
   - Collect dataset for fine-tuning
   - Identify pilot schools
   - Prepare grant applications

---

## 🔗 Resources

- **Full Deployment Guide**: See `Aya_23_Cloud_Deployment_Guide.docx`
- **Automated Script**: Use `quick_deploy_gcp.sh` for one-command setup
- **GitHub Repository**: Complete source code and documentation
- **Technical Spec**: Full architecture and implementation details

---

## 💬 Get Help

- **GitHub Issues**: Report bugs or ask questions
- **Email**: support@sa-edu-llm.org
- **Discord**: [Your community link]

---

**Congratulations! You've successfully deployed Aya 23 to the cloud! 🎉**

*Estimated time: 30 minutes (+ 24-48 hours for GPU quota approval)*
*Free credits cover: ~2 months of 8 hours/day usage*
