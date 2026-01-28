from typing import Dict, Any
from datetime import datetime

class AgentMetrics:
    """Track Agent Performance"""
    def __init__(self):
        self.iterations = 0
        self.tool_calls = 0
        self.tokens_used = 0
        self.search_query = []
        self.errors = []
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        
    def log_tool_call(self, tool_name: str, args: dict):
        self.tool_calls += 1
        if tool_name == "web_search":
            query = args.get('query')
            if query:
                self.search_query.append(query)
            
    def log_error(self, error: str):
        self.errors.append(error)
        
    def get_summary(self) -> Dict[str, Any]:
        duration = (
        (self.end_time - self.start_time).total_seconds() 
        if self.start_time and self.end_time 
        else 0.0
        )
        
        return {
            "iterations": self.iterations,
            "tool_calls": self.tool_calls,
            "search_queries": self.search_query,
            "errors": len(self.errors),
            "duration_seconds": duration,
            "tokens_used": self.tokens_used
        }
    
    def print_summary(self):
        """Pretty print metrics"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("📊 AGENT METRICS")
        print("="*60)
        print(f"⏱️  Duration: {summary['duration_seconds']:.2f}s")
        print(f"🔄 Iterations: {summary['iterations']}")
        print(f"🔧 Tool Calls: {summary['tool_calls']}")
        print(f"🔍 Searches: {len(summary['search_queries'])}")
        if summary['search_queries']:
            for i, query in enumerate(summary['search_queries'], 1):
                print(f"   {i}. {query}")
        print(f"🎫 Tokens Used: {summary['tokens_used']}")
        print(f"❌ Errors: {summary['errors']}")
        print("="*60 + "\n")
        
        return summary