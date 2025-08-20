#!/usr/bin/env python3
"""
n8n Pipeline Monitor - Track execution metrics and data quality
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from collections import defaultdict

# Configuration
N8N_URL = "http://localhost:5678"
N8N_USER = "admin"
N8N_PASSWORD = "maple_tutor_2024"
WORKFLOW_NAME = "Weather to Education Content Pipeline (POC)"

class PipelineMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (N8N_USER, N8N_PASSWORD)
        self.base_url = N8N_URL
        
    def get_executions(self, hours: int = 24) -> List[Dict]:
        """Fetch executions from the last N hours"""
        # Note: n8n API endpoints may vary by version
        # This is a simplified example
        try:
            response = self.session.get(
                f"{self.base_url}/rest/executions",
                params={"limit": 100}
            )
            if response.status_code == 200:
                return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching executions: {e}")
        return []
    
    def analyze_executions(self, executions: List[Dict]) -> Dict:
        """Analyze execution metrics"""
        if not executions:
            return {"error": "No executions found"}
        
        metrics = {
            "total_executions": len(executions),
            "successful": 0,
            "failed": 0,
            "running": 0,
            "average_duration_ms": 0,
            "min_duration_ms": float('inf'),
            "max_duration_ms": 0,
            "errors": defaultdict(int),
            "hourly_distribution": defaultdict(int),
            "cities_processed": defaultdict(int)
        }
        
        total_duration = 0
        
        for execution in executions:
            status = execution.get("status", "unknown")
            
            if status == "success":
                metrics["successful"] += 1
            elif status == "error":
                metrics["failed"] += 1
                error_msg = execution.get("error", {}).get("message", "Unknown error")
                metrics["errors"][error_msg] += 1
            elif status == "running":
                metrics["running"] += 1
            
            # Duration analysis
            if "startedAt" in execution and "stoppedAt" in execution:
                try:
                    start = datetime.fromisoformat(execution["startedAt"])
                    stop = datetime.fromisoformat(execution["stoppedAt"])
                    duration = (stop - start).total_seconds() * 1000  # ms
                    total_duration += duration
                    metrics["min_duration_ms"] = min(metrics["min_duration_ms"], duration)
                    metrics["max_duration_ms"] = max(metrics["max_duration_ms"], duration)
                    
                    # Hourly distribution
                    hour = start.hour
                    metrics["hourly_distribution"][hour] += 1
                except:
                    pass
        
        # Calculate averages
        if metrics["successful"] > 0:
            metrics["average_duration_ms"] = total_duration / metrics["successful"]
            metrics["success_rate"] = (metrics["successful"] / metrics["total_executions"]) * 100
        else:
            metrics["success_rate"] = 0
        
        # Clean up infinity values
        if metrics["min_duration_ms"] == float('inf'):
            metrics["min_duration_ms"] = 0
            
        return metrics
    
    def check_data_quality(self) -> Dict:
        """Check quality of generated content in Airtable"""
        # This would connect to Airtable API to verify data
        # For now, returning placeholder
        return {
            "records_created": "Check Airtable manually",
            "content_quality": "Manual review required",
            "missing_fields": "Check for null values in Airtable"
        }
    
    def generate_report(self, hours: int = 24):
        """Generate monitoring report"""
        print(f"\n{'='*60}")
        print(f"📊 n8n Pipeline Monitor - Last {hours} Hours")
        print(f"{'='*60}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Fetch and analyze executions
        executions = self.get_executions(hours)
        metrics = self.analyze_executions(executions)
        
        if "error" in metrics:
            print(f"❌ {metrics['error']}")
            print("\nPlease ensure:")
            print("1. n8n is running (docker-compose up -d)")
            print("2. Workflow has been executed at least once")
            print("3. Credentials are configured correctly")
            return
        
        # Performance Metrics
        print("📈 Performance Metrics")
        print("-" * 40)
        print(f"Total Executions: {metrics['total_executions']}")
        print(f"✅ Successful: {metrics['successful']}")
        print(f"❌ Failed: {metrics['failed']}")
        print(f"🔄 Running: {metrics['running']}")
        print(f"Success Rate: {metrics['success_rate']:.1f}%")
        print()
        
        # Timing Stats
        print("⏱️ Timing Statistics")
        print("-" * 40)
        print(f"Average Duration: {metrics['average_duration_ms']:.0f}ms")
        print(f"Min Duration: {metrics['min_duration_ms']:.0f}ms")
        print(f"Max Duration: {metrics['max_duration_ms']:.0f}ms")
        target_met = "✅" if metrics['average_duration_ms'] < 30000 else "❌"
        print(f"Target (<30s): {target_met}")
        print()
        
        # Error Analysis
        if metrics['errors']:
            print("⚠️ Error Analysis")
            print("-" * 40)
            for error, count in metrics['errors'].items():
                print(f"  • {error}: {count} times")
            print()
        
        # Hourly Distribution
        if metrics['hourly_distribution']:
            print("📅 Hourly Distribution")
            print("-" * 40)
            for hour in sorted(metrics['hourly_distribution'].keys()):
                count = metrics['hourly_distribution'][hour]
                bar = "█" * count
                print(f"  {hour:02d}:00 | {bar} {count}")
            print()
        
        # Data Quality
        print("✨ Data Quality Check")
        print("-" * 40)
        quality = self.check_data_quality()
        for key, value in quality.items():
            print(f"  • {key}: {value}")
        print()
        
        # Recommendations
        print("💡 Recommendations")
        print("-" * 40)
        
        if metrics['success_rate'] < 90:
            print("  ⚠️ Success rate below 90% - check error logs")
        else:
            print("  ✅ Success rate is good")
            
        if metrics['average_duration_ms'] > 30000:
            print("  ⚠️ Average execution time exceeds 30s target")
            print("     Consider optimizing API calls or adding caching")
        else:
            print("  ✅ Execution time within target")
            
        if metrics['failed'] > metrics['successful'] * 0.1:
            print("  ⚠️ High error rate detected - investigate failures")
            
        print()
        print("📋 Next Steps:")
        print("  1. Review any errors in n8n execution history")
        print("  2. Check Airtable for data completeness")
        print("  3. Verify content quality manually")
        print("  4. Monitor OpenAI API usage and costs")
        print()

def main():
    """Main monitoring function"""
    monitor = PipelineMonitor()
    
    # Check command line arguments
    hours = 24
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [hours]")
            print(f"Example: {sys.argv[0]} 24")
            sys.exit(1)
    
    monitor.generate_report(hours)

if __name__ == "__main__":
    main()