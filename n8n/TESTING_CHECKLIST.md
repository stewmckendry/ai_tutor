# n8n Pipeline Testing Checklist

## 🚀 Pre-Launch Checklist

### Environment Setup
- [ ] Docker installed and running
- [ ] n8n container started (`./setup.sh`)
- [ ] Can access n8n at http://localhost:5678
- [ ] Logged in with credentials

### Credentials Configuration
- [ ] OpenAI API key added to n8n
- [ ] OpenAI key has GPT-3.5-turbo access
- [ ] Airtable Personal Access Token added
- [ ] Airtable token has write permissions
- [ ] Airtable base ID configured

### Airtable Setup
- [ ] Dynamic_Content_Test table created
- [ ] All required fields added (see airtable_schema.md)
- [ ] Field types match specification
- [ ] Test manual record creation works

### Workflow Import
- [ ] weather_to_education_poc.json imported
- [ ] All nodes show in workflow
- [ ] No missing credential warnings
- [ ] Connections between nodes visible

## 🧪 Manual Testing Phase

### Test 1: Weather Fetching
- [ ] Execute workflow manually
- [ ] Toronto weather node returns data
- [ ] Vancouver weather node returns data
- [ ] Check XML contains temperature
- [ ] Verify RSS feeds accessible

### Test 2: Data Parsing
- [ ] Parse Weather Data node executes
- [ ] Temperature extracted correctly
- [ ] Condition extracted correctly
- [ ] City identified correctly
- [ ] Timestamp generated

### Test 3: OpenAI Enrichment
- [ ] OpenAI node executes without error
- [ ] Response contains all required fields
- [ ] Content is Grade 4 appropriate
- [ ] Canadian spelling used
- [ ] Science connection relevant

### Test 4: Airtable Storage
- [ ] Airtable node executes successfully
- [ ] Record created in Dynamic_Content_Test
- [ ] All fields populated correctly
- [ ] No data truncation
- [ ] Timestamp accurate

### Test 5: Error Handling
- [ ] Error Handler node executes
- [ ] Status logged correctly
- [ ] Workflow completes even with errors
- [ ] Error details captured

## 📊 Load Testing Phase

### 10-Run Test
- [ ] Run workflow 10 times manually
- [ ] Success rate >= 90%
- [ ] Average execution time < 30s
- [ ] No duplicate records in Airtable
- [ ] Content variety (not identical)

### Data Quality Validation
```bash
python validate_data.py
```
- [ ] All required fields present
- [ ] Canadian spelling consistent
- [ ] Temperature values reasonable
- [ ] Educational content appropriate
- [ ] Science connections valid

### Performance Monitoring
```bash
python monitor.py
```
- [ ] Execution metrics collected
- [ ] Error patterns identified
- [ ] Timing within targets
- [ ] Resource usage acceptable

## ⏰ Scheduled Testing Phase

### Enable Schedule
- [ ] Activate "Every Hour" trigger node
- [ ] Set workflow to Active
- [ ] Verify first scheduled run
- [ ] Check execution logs

### 24-Hour Test
- [ ] Let run for full 24 hours
- [ ] Monitor every 4-6 hours
- [ ] Document any failures
- [ ] Check Airtable growth

### Success Metrics
- [ ] Total executions: 24 ± 2
- [ ] Success rate: > 90%
- [ ] Average time: < 30 seconds
- [ ] Data quality score: > 80/100
- [ ] No critical errors

## 🐛 Common Issues & Solutions

### Issue: Weather fetch fails
- Check RSS URLs in browser
- Verify no firewall blocking
- Try alternative Environment Canada endpoints

### Issue: OpenAI timeout
- Increase timeout in node settings (30s → 60s)
- Check API key validity
- Verify API quota not exceeded

### Issue: Airtable permission denied
- Regenerate Personal Access Token
- Ensure token has data.records:write scope
- Verify base ID correct

### Issue: JSON parse errors
- Check OpenAI response format
- Add fallback parsing in code node
- Log raw response for debugging

### Issue: Duplicate records
- Add deduplication logic
- Check schedule trigger intervals
- Implement idempotency key

## 📈 Metrics to Track

### Execution Metrics
- Success/failure ratio
- Average execution time
- Peak execution time
- Error frequency by type

### Data Metrics
- Records created per hour
- Content quality score
- Field completion rate
- Canadian spelling accuracy

### Cost Metrics
- OpenAI tokens used
- Estimated monthly cost
- Airtable API calls
- Storage growth rate

## ✅ Final Validation

### Before Production
- [ ] All tests passed
- [ ] Documentation complete
- [ ] Error handling robust
- [ ] Monitoring in place
- [ ] Costs within budget

### Sign-off Criteria
- [ ] 24-hour test successful
- [ ] Quality score > 80%
- [ ] Stakeholder review complete
- [ ] Next steps documented
- [ ] Lessons learned captured

## 📝 Test Results Log

### Test Run 1
- Date: ___________
- Duration: ___________
- Success Rate: ___________
- Issues Found: ___________
- Notes: ___________

### Test Run 2
- Date: ___________
- Duration: ___________
- Success Rate: ___________
- Issues Found: ___________
- Notes: ___________

### 24-Hour Test
- Start: ___________
- End: ___________
- Total Executions: ___________
- Successful: ___________
- Failed: ___________
- Quality Score: ___________
- Decision: [ ] Proceed [ ] Iterate [ ] Redesign

## 🚀 Next Steps After Testing

1. **If Successful (>90% success rate)**
   - Document lessons learned
   - Plan expansion (more cities)
   - Design production architecture
   - Estimate scaling costs

2. **If Partially Successful (70-90%)**
   - Identify failure patterns
   - Optimize problem areas
   - Rerun targeted tests
   - Adjust error handling

3. **If Unsuccessful (<70%)**
   - Review architecture
   - Consider alternatives
   - Identify root causes
   - Redesign problem components

## 📞 Support Resources

- n8n Documentation: https://docs.n8n.io
- n8n Community: https://community.n8n.io
- OpenAI Status: https://status.openai.com
- Airtable Status: https://status.airtable.com
- Environment Canada: https://weather.gc.ca/business/index_e.html