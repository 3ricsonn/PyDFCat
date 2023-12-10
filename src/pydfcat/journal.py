# -*- coding: utf-8 -*-
from typing import Optional

import fitz  # PyMuPDF
from io import BytesIO


__all__ = ["_JournalDocument"]

_history_entry_type = tuple[str, fitz.Document, list[int]]


class _JournalDocument:
    # ether mod | pages | index or mode | pages
    __history: list[_history_entry_type] = []
    __document: fitz.Document
    __pointer: int = 0

    @property
    def document(self) -> fitz.Document:
        return self.__document

    def __init__(self, file_path: Optional[str] = None) -> None:
        self.__document = fitz.Document(file_path)
        self.create_snapshot()

    def insert(self, index: int, pages: fitz.Document) -> None:
        self.__pointer += 1
        index = index if index != -1 else len(self.__document)
        self.__document.insert_pdf(pages, start_at=index)
        self.__history.insert(
            self.__pointer, ("insert", pages, list(range(index, index + len(pages))))
        )

    def delete(self, index: list[int]) -> None:
        self.__pointer += 1
        self.__document.delete_pages(index)
        self.__history.insert(
            self.__pointer, ("delete", self.copy_pages(index=index), index)
        )

    def create_snapshot(self) -> None:
        self.__pointer += 1
        self.__history.insert(self.__pointer, ("snapshot", self.copy_pages(), []))

    def forward(self) -> _history_entry_type:
        if self.__pointer < len(self.__history):
            self.__pointer += 1
            history_entry = self.__history[self.__pointer]

            if history_entry[0] == "insert":
                self.__document.insert_pdf(history_entry[1], start_at=history_entry[2])
            elif history_entry[0] == "delete":
                self.__document.delete_pages(history_entry[2])

            return history_entry
        else:
            return "start", self.__document, []

    def backward(self) -> _history_entry_type:
        if self.__pointer > 0:
            history_entry = self.__history[self.__pointer]

            if history_entry[0] == "insert":
                self.__document.delete_pages(history_entry[2])
            elif history_entry[0] == "delete":
                for page, index in zip(history_entry[1], history_entry[2]):
                    self.__document.insert_pdf(page, start_at=index)

            self.__pointer -= 1

            return history_entry
        else:
            return "end", self.__document, []

    def copy_pages(self, index: Optional[list[int]] = None) -> fitz.Document:
        if len(self.__document) > 0:
            doc_buffer = BytesIO(self.__document.write(garbage=4))
            doc = fitz.Document(stream=doc_buffer, filetype="pdf")

            if index:
                doc.select(index)
                return doc
            else:
                return doc
        else:
            return fitz.Document()
