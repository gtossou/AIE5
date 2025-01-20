import os
import fitz  # PyMuPDF
from collections import defaultdict
from typing import List


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.path = path
        self.encoding = encoding
        self.documents = []

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory(self.path)
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        elif os.path.isfile(self.path) and self.path.endswith(".pdf"):
            self.load_pdf()
        else:
            raise ValueError(f"Unsupported file type: {self.path}")

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as file:
            self.documents.append(file.read())

    def load_pdf(self):
        doc = fitz.open(self.path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.documents.append(text)

    def load_directory(self, directory_path: str):
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(".txt"):
                    self.load_file(file_path)
                elif file_path.endswith(".pdf"):
                    self.load_pdf(file_path)

    def load_documents(self):
        self.load()
        return self.documents
    
class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
