import aiofiles
from typing import Optional

class TextExtractor:
    async def extract_from_file(self, file_path: str) -> str:
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                content = await file.read()
            return content
        except UnicodeDecodeError:
            # Try with different encoding
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as file:
                content = await file.read()
            return content
        except Exception as e:
            raise Exception(f"Failed to extract text from file: {str(e)}")