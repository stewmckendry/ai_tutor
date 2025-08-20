# n8n Content Pipeline - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- OpenAI API key ([Get API Key](https://platform.openai.com/api-keys))
- Airtable Personal Access Token ([Get Token](https://airtable.com/create/tokens))

### Step 1: Start n8n
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Step 2: Access n8n
Open browser: http://localhost:5678
- Username: `admin`
- Password: `maple_tutor_2024`

### Step 3: Import Workflow
1. Click **Workflows** → **New**
2. Menu (⋮) → **Import from File**
3. Select `workflows/weather_to_education_poc.json`

### Step 4: Add Credentials

#### OpenAI
1. Click any OpenAI node in workflow
2. Credentials dropdown → **Create New**
3. Enter your OpenAI API key
4. Name: "OpenAI API"
5. Save

#### Airtable
1. Click the Airtable node
2. Credentials dropdown → **Create New**
3. Enter your Personal Access Token
4. Name: "Airtable API"
5. Save

### Step 5: Configure Airtable Base
1. In Airtable node, enter your Base ID
2. Table should be "Dynamic_Content_Test"
3. If table doesn't exist, create it using `airtable_schema.md`

### Step 6: Test
1. Click **Execute Workflow** button
2. Check green ✓ on each node
3. Verify record in Airtable

### Step 7: Schedule (Optional)
1. Click "Every Hour" trigger node
2. Toggle Disabled → Enabled
3. Save workflow
4. Click **Active** toggle (top-right)

## 📁 Files

```
n8n/
├── docker-compose.yml     # Docker configuration
├── setup.sh              # Setup script
├── README.md            # This file
├── airtable_schema.md   # Table structure
├── credentials.env.example # Example credentials
├── workflows/
│   └── weather_to_education_poc.json  # n8n workflow
└── n8n_data/           # n8n data (created on first run)
```

## 🔧 Common Commands

```bash
# Start n8n
docker-compose up -d

# Stop n8n
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Clean restart (removes data)
docker-compose down -v
docker-compose up -d
```

## 🏗️ Airtable Table Setup

Create table `Dynamic_Content_Test` with these fields:

| Field | Type | Required |
|-------|------|----------|
| record_id | Autonumber | Auto |
| location | Single line text | Yes |
| temperature | Number | Yes |
| condition | Single line text | Yes |
| raw_weather | Long text | Yes |
| enriched_content | Long text | Yes |
| science_connection | Long text | Yes |
| activity_suggestion | Long text | Yes |
| fun_fact | Long text | No |
| vocabulary_word | Long text | No |
| workflow_version | Single line text | Yes |
| pipeline_timestamp | Date and time | Yes |
| created_at | Created time | Auto |
| updated_at | Last modified time | Auto |

## 🎯 What This Does

Every hour (or on-demand):
1. **Fetches** weather from Toronto & Vancouver
2. **Enriches** with OpenAI to create Grade 4 content
3. **Stores** in Airtable for the AI tutor to use

### Sample Output
```
Location: Toronto
Temp: 5°C
Educational Content: "It's 5°C in Toronto - as cold as your fridge! 
Clouds act like Earth's blanket, keeping heat from escaping."
Activity: "Compare temperatures in sun vs shade to see how clouds affect heat!"
```

## 💰 Costs

- **OpenAI**: ~$0.72/month (hourly updates)
- **Airtable**: Free tier (up to 1,200 records)
- **n8n**: Free (self-hosted)

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't access http://localhost:5678 | Check Docker is running: `docker ps` |
| Workflow fails at OpenAI | Verify API key has GPT-3.5 access |
| Airtable error | Check token has write permissions |
| Weather fetch fails | RSS feeds might be down, check URLs in browser |

## 📊 Monitor Success

After 24 hours, check:
- ✅ 20+ successful executions
- ⏱️ Average time < 30 seconds
- 📝 Quality content in Airtable
- ❌ Error rate < 10%

## 🚀 Next Steps

Once POC succeeds:
1. Add more Canadian cities
2. Include sports & news data
3. Enhance AI prompts
4. Add monitoring dashboard

## 📚 Documentation

- Full docs: `../docs/n8n_pipeline.md`
- Airtable schema: `airtable_schema.md`
- Main project: `../README.md`