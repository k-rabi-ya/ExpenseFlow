"""
API client service for frontend integration
"""
import axios
from typing import List, Dict, Any

# Configure API base URL
API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000"

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

class ExpenseFlowAPI {
    @staticmethod
    async categorize(description: str) -> Dict[str, Any]:
        """Categorize a single transaction"""
        response = await apiClient.post("/api/categorize", {
            description: description
        })
        return response.data

    @staticmethod
    async batch_categorize(descriptions: List[str]) -> Dict[str, Any]:
        """Categorize multiple transactions"""
        response = await apiClient.post("/api/batch-categorize", {
            descriptions: descriptions
        })
        return response.data

    @staticmethod
    async import_csv(file: File) -> Dict[str, Any]:
        """Import and categorize from CSV"""
        form_data = new FormData()
        form_data.append("file", file)
        response = await apiClient.post("/api/import", form_data, {
            headers: {"Content-Type": "multipart/form-data"}
        })
        return response.data

    @staticmethod
    async ocr_categorize(file: File) -> Dict[str, Any]:
        """Extract from receipt and categorize"""
        form_data = new FormData()
        form_data.append("file", file)
        response = await apiClient.post("/api/ocr-categorize", form_data, {
            headers: {"Content-Type": "multipart/form-data"}
        })
        return response.data

    @staticmethod
    async record_correction(transaction_id: int, correct_category: str) -> Dict[str, Any]:
        """Record user correction"""
        response = await apiClient.post("/api/correct", {
            transaction_id: transaction_id,
            correct_category: correct_category
        })
        return response.data

export default ExpenseFlowAPI
