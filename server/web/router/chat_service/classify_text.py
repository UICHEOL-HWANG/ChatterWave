import httpx
from typing import List, Dict
from fastapi import HTTPException
import asyncio

# 혐오 표현 감지 API URL
CLASSIFY_API_ENDPOINT = "http://proxy-server/model_api/api/inference/classify"


async def classify_text(texts: List[str]) -> List[Dict[str, str]]:
    """
    혐오 표현 감지 API 호출

    Args:
        texts (List[str]): 감지할 텍스트 리스트

    Returns:
        List[Dict[str, str]]: 감지 결과 (label과 score 포함)
    """
    try:
        payload = {"texts": texts}
        async with httpx.AsyncClient() as client:
            response = await client.post(CLASSIFY_API_ENDPOINT, json=payload, timeout=10)
            response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during classification: {str(e)}")

