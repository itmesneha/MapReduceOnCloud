# 🎉 Full Cloud Deployment Complete!

Your MapReduce application is now fully deployed on AWS!

## 🌐 Application URLs

### Frontend (S3 Static Website)
**Website URL:** http://sneha-lab1-photo-public.s3-website-ap-southeast-1.amazonaws.com/frontend/index.html

⚠️ **Important:** Use the HTTP URL above, not the HTTPS S3 URL. The backend is HTTP-only, and browsers block mixed content (HTTPS frontend calling HTTP API).

### Backend (EC2)
**API Documentation:** http://18.138.254.59:8000/docs
**API Endpoint:** http://18.138.254.59:8000
**Test Endpoint:** http://18.138.254.59:8000/user/1

### Dataset (S3)
**S3 URI:** s3://sneha-lab1-photo-public/twitter_combined.txt
**Public URL:** https://sneha-lab1-photo-public.s3.ap-southeast-1.amazonaws.com/twitter_combined.txt

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User's Browser                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              S3 Static Website (Frontend)                    │
│         sneha-lab1-photo-public/frontend/                   │
│              - index.html                                    │
│              - style.css                                     │
│              - script.js                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP API Calls
                           ↓
┌─────────────────────────────────────────────────────────────┐
│         EC2 Instance (18.138.254.59)                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Docker Container (FastAPI)                 │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │    PySpark MapReduce Engine                  │  │    │
│  │  │         ↓ Reads from                         │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │ S3 API
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              S3 Bucket (Dataset Storage)                     │
│         sneha-lab1-photo-public/                            │
│              twitter_combined.txt (44M+ edges)              │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Deployment Details

### Frontend Deployment
- **Hosting:** AWS S3 Static Website
- **Region:** ap-southeast-1 (Singapore)
- **Files:** 3 files (HTML, CSS, JS)
- **Access:** Public read via bucket policy

### Backend Deployment
- **Instance:** EC2 i-061b4f063cfae29c3 (t3.micro)
- **OS:** Ubuntu 24.04 LTS
- **Container:** Docker with FastAPI + PySpark
- **Java Version:** OpenJDK 21
- **Python Version:** 3.11
- **Auto-deployment:** GitHub Actions on push to main

### Dataset Storage
- **Storage:** S3 Bucket
- **Size:** ~500MB compressed Twitter network data
- **Access:** Public read via bucket policy
- **Format:** Edge list (userA userB)

## 🔄 Auto-Deployment Workflow

Every time you push to the `main` branch:

1. ✅ GitHub Actions triggers
2. ✅ SSH into EC2 instance
3. ✅ Pull latest code
4. ✅ Build Docker image
5. ✅ Deploy new containers
6. ✅ Run health checks

## 📝 Manual Deployment Commands

### Update Frontend
```bash
cd /Users/snehas/Documents/GitHub/MapReduceOnCloud
aws s3 sync frontend/ s3://sneha-lab1-photo-public/frontend/ --delete
```

### Update Backend
```bash
git add .
git commit -m "Update backend"
git push origin main
# GitHub Actions will auto-deploy!
```

### Update Dataset
```bash
aws s3 cp backend/twitter_combined.txt s3://sneha-lab1-photo-public/twitter_combined.txt
```

## 🔧 Testing Your Application

### Test Frontend
Visit: http://sneha-lab1-photo-public.s3-website-ap-southeast-1.amazonaws.com/frontend/index.html

1. Enter a user ID (e.g., `1`, `12`, `100`)
2. Click "Fetch Stats"
3. See follower/followee counts

### Test Backend API
```bash
# Health check
curl http://18.138.254.59:8000/docs

# Get user stats
curl http://18.138.254.59:8000/user/1
```

### Test S3 Dataset Access
```bash
# Check if dataset is accessible
curl -I https://sneha-lab1-photo-public.s3.ap-southeast-1.amazonaws.com/twitter_combined.txt
```

## 💰 Cost Breakdown (Approximate)

### EC2 Instance (t3.micro)
- **Running 24/7:** ~$7-8/month
- **Stopped:** $0/hour (only pay for storage ~$0.80/month)

### S3 Storage
- **500MB dataset:** ~$0.01/month
- **Frontend files:** <$0.01/month
- **Data transfer:** First 1GB/month free

### Total Monthly Cost
- **If running 24/7:** ~$8/month
- **If stopped when not in use:** <$1/month

## 🔒 Security Configuration

### EC2 Security Group (sg-0cca911e6657cc8c0)
- Port 22 (SSH): Open to 0.0.0.0/0 (for GitHub Actions)
- Port 8000 (API): Open to 0.0.0.0/0 (for frontend access)
- Port 80 (HTTP): Open to 0.0.0.0/0

### S3 Bucket Policy
- Frontend files: Public read access
- Dataset: Public read access
- All other operations: Denied

## 🎯 Performance Notes

### PySpark Processing
- **Mode:** Local mode (single machine)
- **Dataset Size:** 44M+ edges
- **First Request:** ~30-60 seconds (loads entire dataset)
- **Subsequent Requests:** Instant (cached in memory)

### S3 Data Transfer
- **Read Speed:** ~25-100 MB/s from EC2 to S3 (same region)
- **No egress charges:** EC2 and S3 in same region

## 🐛 Troubleshooting

### Frontend not loading
```bash
# Check S3 website configuration
aws s3api get-bucket-website --bucket sneha-lab1-photo-public

# Verify bucket policy
aws s3api get-bucket-policy --bucket sneha-lab1-photo-public
```

### Backend not responding
```bash
# SSH into EC2
ssh -i /Users/snehas/my-cli-key.pem ubuntu@18.138.254.59

# Check container status
cd ~/MapReduceOnCloud/deployment
sudo docker-compose ps
sudo docker-compose logs backend
```

### Dataset not accessible
```bash
# Verify S3 object exists
aws s3 ls s3://sneha-lab1-photo-public/

# Test public access
curl -I https://sneha-lab1-photo-public.s3.ap-southeast-1.amazonaws.com/twitter_combined.txt
```

## 🚦 Next Steps

1. ✅ **Test the application** - Visit the frontend URL
2. ✅ **Monitor the first request** - May take 30-60 seconds to load dataset
3. ⭐ **Optional: Add custom domain** - Use Route53 for better URLs
4. ⭐ **Optional: Add CloudFront** - CDN for faster frontend delivery
5. ⭐ **Optional: Add HTTPS** - SSL certificate for secure access
6. ⭐ **Optional: Add CloudWatch** - Monitor API usage and errors

## 📚 Documentation Files

- **GitHub Actions Setup:** `deployment/GITHUB_ACTIONS_SETUP.md`
- **EC2 Setup:** `deployment/ec2_setup_instructions.md`
- **Quick Start:** `deployment/QUICKSTART.md`
- **Backend README:** `backend/README.md`

## 🎉 Congratulations!

Your MapReduce Twitter application is now fully deployed on AWS Cloud with:
- ✅ Frontend hosted on S3
- ✅ Backend running on EC2 with Docker
- ✅ Dataset stored in S3
- ✅ Auto-deployment via GitHub Actions
- ✅ Scalable PySpark processing

**Main Application URL:**
http://sneha-lab1-photo-public.s3-website-ap-southeast-1.amazonaws.com/frontend/index.html

Enjoy your cloud-native MapReduce application! 🚀
