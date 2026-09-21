from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    @abstractmethod
    async def generate_insights(self, metrics: Dict[str, Any], dataset_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def answer_question(self, question: str, context: Dict[str, Any], data_summary: Dict[str, Any]) -> str:
        pass
        
    @abstractmethod
    async def classify_dataset(self, columns: List[str], sample_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    async def generate_report_summary(self, analysis_data: Dict[str, Any]) -> str:
        pass
