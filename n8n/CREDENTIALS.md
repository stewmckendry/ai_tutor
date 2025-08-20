# n8n Credentials for Configuration

## 🌐 Access n8n
- **URL**: http://localhost:5678
- **Status**: ✅ Running (existing container)

## 🔑 API Credentials

### OpenAI API
**When creating OpenAI credential in n8n:**
```
sk-proj-[YOUR-OPENAI-API-KEY]
```

### Airtable API
**When creating Airtable credential in n8n:**

**Personal Access Token:**
```
pat[YOUR-AIRTABLE-PERSONAL-ACCESS-TOKEN]
```

**Base ID (Maple Grade 4 Science Base):**
```
app1FNYWApMBYHob0
```

**Table Name:**
```
Dynamic_Content_Test
```

**Table ID (auto-created):**
```
tblPNfN103WTygeub
```

## 📋 Setup Steps

1. **Open n8n**: http://localhost:5678

2. **Import Workflow**:
   - Click **Workflows** → **New**
   - Menu (⋮) → **Import from File**
   - Select: `/Users/liammckendry/ai_tutor_worktrees/issue-18/n8n/workflows/weather_to_education_poc.json`

3. **Configure OpenAI**:
   - Click any OpenAI node in workflow
   - Credentials dropdown → **Create New**
   - Paste the OpenAI API key above
   - Name: "OpenAI API"
   - Save

4. **Configure Airtable**:
   - Click the Airtable node
   - Credentials dropdown → **Create New**
   - Select "Airtable API Token"
   - Paste the Personal Access Token above
   - Name: "Airtable API"
   - Save
   - In the node, Base ID should auto-populate or paste: `app1FNYWApMBYHob0`
   - Table should be: `Dynamic_Content_Test`

5. **Test Workflow**:
   - Click **Execute Workflow** button
   - Check for green ✓ on each node
   - Verify record created in Airtable

## ✅ Table Created

The `Dynamic_Content_Test` table has been created in the Thunder Hockey Airtable base with these fields:
- location
- temperature
- condition
- raw_weather
- enriched_content
- science_connection
- activity_suggestion
- fun_fact
- vocabulary_word
- workflow_version
- pipeline_timestamp

## 🔍 Verify Setup

Check the table in Airtable:
1. Go to: https://airtable.com/app1FNYWApMBYHob0
2. Look for "Dynamic_Content_Test" table
3. Verify all fields are present

## 🚨 Troubleshooting

If credentials don't work:
- Verify keys haven't expired
- Check API quotas/limits
- Ensure Airtable token has write permissions
- Confirm OpenAI has GPT-3.5 access