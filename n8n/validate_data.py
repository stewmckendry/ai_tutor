#!/usr/bin/env python3
"""
Validate data quality in Airtable Dynamic_Content_Test table
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

# Configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = 'Dynamic_Content_Test'

class DataValidator:
    def __init__(self):
        if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
            print("❌ Missing Airtable credentials in .env file")
            print("Please set AIRTABLE_API_KEY and AIRTABLE_BASE_ID")
            sys.exit(1)
            
        self.table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, TABLE_NAME)
        
    def fetch_recent_records(self, hours: int = 24) -> List[Dict]:
        """Fetch records from the last N hours"""
        try:
            # Fetch all records (Airtable doesn't support date filtering in API)
            records = self.table.all()
            
            # Filter by date if pipeline_timestamp exists
            cutoff = datetime.now() - timedelta(hours=hours)
            recent_records = []
            
            for record in records:
                fields = record.get('fields', {})
                timestamp_str = fields.get('pipeline_timestamp')
                
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if timestamp > cutoff:
                            recent_records.append(record)
                    except:
                        pass
                else:
                    # Include records without timestamp (might be manual tests)
                    recent_records.append(record)
                    
            return recent_records
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []
    
    def validate_record(self, record: Dict) -> Dict:
        """Validate a single record for data quality"""
        fields = record.get('fields', {})
        record_id = record.get('id', 'unknown')
        
        issues = []
        warnings = []
        
        # Required fields
        required_fields = [
            'location',
            'temperature',
            'condition',
            'enriched_content',
            'science_connection',
            'activity_suggestion'
        ]
        
        for field in required_fields:
            if field not in fields or not fields[field]:
                issues.append(f"Missing required field: {field}")
        
        # Validate temperature is numeric
        if 'temperature' in fields:
            temp = fields['temperature']
            if not isinstance(temp, (int, float)):
                issues.append(f"Temperature is not numeric: {temp}")
            elif temp < -50 or temp > 50:
                warnings.append(f"Temperature seems unrealistic: {temp}°C")
        
        # Validate location
        if 'location' in fields:
            location = fields['location']
            if location not in ['Toronto', 'Vancouver']:
                warnings.append(f"Unexpected location: {location}")
        
        # Content quality checks
        if 'enriched_content' in fields:
            content = fields['enriched_content']
            if len(content) < 50:
                warnings.append("Educational content seems too short")
            if len(content) > 500:
                warnings.append("Educational content seems too long")
            
            # Check for Grade 4 appropriate language
            complex_words = ['sophisticated', 'elaborate', 'comprehensive', 'intricate']
            for word in complex_words:
                if word.lower() in content.lower():
                    warnings.append(f"Complex word '{word}' may not be Grade 4 appropriate")
        
        # Check Canadian spelling
        if 'enriched_content' in fields:
            content = fields['enriched_content']
            us_spellings = {
                'color': 'colour',
                'center': 'centre',
                'favorite': 'favourite',
                'honor': 'honour'
            }
            for us, ca in us_spellings.items():
                if us in content and ca not in content:
                    warnings.append(f"US spelling '{us}' should be '{ca}'")
        
        # Check science connection
        if 'science_connection' in fields:
            connection = fields['science_connection']
            science_keywords = ['light', 'sound', 'heat', 'temperature', 'energy', 'matter']
            has_science = any(keyword in connection.lower() for keyword in science_keywords)
            if not has_science:
                warnings.append("Science connection doesn't mention key concepts")
        
        return {
            'record_id': record_id,
            'location': fields.get('location', 'unknown'),
            'timestamp': fields.get('pipeline_timestamp', 'unknown'),
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    def generate_report(self, hours: int = 24):
        """Generate data quality report"""
        print(f"\n{'='*60}")
        print(f"📊 Airtable Data Quality Report - Last {hours} Hours")
        print(f"{'='*60}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Table: {TABLE_NAME}")
        print(f"{'='*60}\n")
        
        # Fetch and validate records
        records = self.fetch_recent_records(hours)
        
        if not records:
            print("❌ No records found in the specified time period")
            print("\nPossible reasons:")
            print("1. Table doesn't exist yet - create using airtable_schema.md")
            print("2. No workflow executions yet - run workflow first")
            print("3. Wrong credentials - check .env file")
            return
        
        # Validate each record
        validations = [self.validate_record(record) for record in records]
        
        # Summary statistics
        total = len(validations)
        valid = sum(1 for v in validations if v['valid'])
        with_warnings = sum(1 for v in validations if v['warnings'])
        
        print("📈 Summary Statistics")
        print("-" * 40)
        print(f"Total Records: {total}")
        print(f"✅ Valid Records: {valid} ({valid/total*100:.1f}%)")
        print(f"⚠️ Records with Warnings: {with_warnings}")
        print(f"❌ Invalid Records: {total - valid}")
        print()
        
        # Location distribution
        locations = {}
        for v in validations:
            loc = v['location']
            locations[loc] = locations.get(loc, 0) + 1
        
        print("📍 Location Distribution")
        print("-" * 40)
        for location, count in sorted(locations.items()):
            print(f"  {location}: {count} records")
        print()
        
        # Issues breakdown
        all_issues = []
        all_warnings = []
        for v in validations:
            all_issues.extend(v['issues'])
            all_warnings.extend(v['warnings'])
        
        if all_issues:
            print("❌ Critical Issues")
            print("-" * 40)
            issue_counts = {}
            for issue in all_issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {issue}: {count} times")
            print()
        
        if all_warnings:
            print("⚠️ Quality Warnings")
            print("-" * 40)
            warning_counts = {}
            for warning in all_warnings:
                warning_type = warning.split(':')[0]
                warning_counts[warning_type] = warning_counts.get(warning_type, 0) + 1
            for warning, count in sorted(warning_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {warning}: {count} times")
            print()
        
        # Sample content
        print("📝 Sample Content (Most Recent)")
        print("-" * 40)
        if validations:
            recent = validations[0]
            record = records[0]['fields']
            print(f"Location: {record.get('location', 'N/A')}")
            print(f"Temperature: {record.get('temperature', 'N/A')}°C")
            print(f"Condition: {record.get('condition', 'N/A')}")
            print(f"\nEducational Content:")
            print(f"  {record.get('enriched_content', 'N/A')[:200]}...")
            print(f"\nScience Connection:")
            print(f"  {record.get('science_connection', 'N/A')}")
            print(f"\nActivity:")
            print(f"  {record.get('activity_suggestion', 'N/A')}")
        print()
        
        # Quality score
        quality_score = (valid / total * 50) + ((total - len(all_warnings)/2) / total * 50)
        
        print("🏆 Overall Quality Score")
        print("-" * 40)
        print(f"Score: {quality_score:.1f}/100")
        
        if quality_score >= 90:
            print("Rating: Excellent ⭐⭐⭐⭐⭐")
        elif quality_score >= 80:
            print("Rating: Good ⭐⭐⭐⭐")
        elif quality_score >= 70:
            print("Rating: Acceptable ⭐⭐⭐")
        else:
            print("Rating: Needs Improvement ⭐⭐")
        
        print()
        print("💡 Recommendations")
        print("-" * 40)
        
        if valid < total:
            print("  ⚠️ Some records have missing required fields")
            print("     Check n8n workflow data mappings")
        
        if 'US spelling' in str(all_warnings):
            print("  ⚠️ US spellings detected - update OpenAI prompt")
            print("     to emphasize Canadian spelling")
        
        if with_warnings > total * 0.3:
            print("  ⚠️ Many quality warnings - review OpenAI prompt")
            print("     for Grade 4 appropriateness")
        
        if quality_score >= 90:
            print("  ✅ Data quality is excellent!")
            print("     Ready for production testing")
        
        print()

def main():
    """Main validation function"""
    validator = DataValidator()
    
    # Check command line arguments
    hours = 24
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [hours]")
            print(f"Example: {sys.argv[0]} 24")
            sys.exit(1)
    
    validator.generate_report(hours)

if __name__ == "__main__":
    main()