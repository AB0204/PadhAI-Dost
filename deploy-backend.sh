#!/bin/bash

echo "🚀 Deploying PadhAI Dost Backend..."

# 1. Login to Railway
echo "🔓 Step 1: Checking Railway Login..."
if railway whoami >/dev/null 2>&1; then
    echo "✅ Already logged in."
else
    echo "🔓 Log in to Railway (Opens in browser)..."
    railway login
fi

# 2. Link Project
echo "🔗 Step 2: Linking Railway Project..."
# Try to link to existing 'PadhAI-Dost' or create it if missing
railway link --project PadhAI-Dost || railway init --name PadhAI-Dost

# 3. Set Env Vars
echo "🔑 Step 3: Setting Environment Variables..."
echo "INFO: Skipping API Key for Demo Mode."
# We explicitly do NOT set the key, or set it to empty if needed.
# railway vars set GEMINI_API_KEY="" 

# 4. Deploy
echo "☁️ Step 4: Pushing to Cloud..."
railway up

echo "✅ Backend Deployment Initiated!"
echo "👉 Once complete, copy the Railway URL and update NEXT_PUBLIC_API_URL in your frontend."
