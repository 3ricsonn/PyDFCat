# -*- coding: utf-8 -*-
from typing import Optional

import fitz
from io import BytesIO


_journal_entry_type = tuple[str, Optional[fitz.Document], list[int], list[int]]


class _JournalObject:
    __journal: list[tuple[_journal_entry_type, _journal_entry_type]] = []
    __pointer: int = -1

    @property
    def current(self) -> tuple[_journal_entry_type, _journal_entry_type]:
        return self.__journal[self.__pointer]

    def insert(
        self, main_entry: _journal_entry_type, clipboard_entry: _journal_entry_type
    ) -> None:
        self.__pointer += 1
        if self.__pointer < len(self.__journal) - 1:
            self.__journal.pop(self.__pointer)
        self.__journal.insert(self.__pointer, (main_entry, clipboard_entry))
        print(self.__pointer, (main_entry, clipboard_entry))

    def forward(self) -> tuple[_journal_entry_type, _journal_entry_type]:
        if self.__pointer < len(self.__journal):
            self.__pointer += 1

        return self.__journal[self.__pointer]

    def backward(self) -> tuple[_journal_entry_type, _journal_entry_type]:
        history_entry = self.__journal[self.__pointer]
        if self.__pointer > 0:
            self.__pointer -= 1

        return history_entry


class _JournalDocument:
    __document: fitz.Document

    @property
    def document(self):
        return self.__document

    def __init__(self, journal: _JournalObject, file_path: Optional[str] = None):
        self.__journal = journal

        if file_path:
            self.__document = fitz.Document(file_path)
            self.type = 1
        else:
            self.__document = fitz.Document()
            self.type = 0

        self.create_snapshot()

    def insert(
        self,
        index: int,
        pages: fitz.Document,
        append_entry: Optional[_journal_entry_type] = None,
    ) -> None:
        index = index if index != -1 else len(self.__document)
        self.__document.insert_pdf(pages, start_at=index)

        # entry: type | changed pages | changed pages position | selected pages
        entry: list[_journal_entry_type] = [
            (
                "insert",
                pages,
                list(range(index, index + len(pages))),
                list(range(index, index + len(pages))),
            )
        ]
        entry.insert(self.type, append_entry)
        self.__journal.insert(*entry)

    def delete(
        self, indexes: list[int], append_entry: Optional[_journal_entry_type] = None
    ):
        self.__document.delete_pages(indexes)

        # entry: type | changed pages | changed pages position | selected pages
        entry: list[_journal_entry_type] = [
            (
                "delete",
                self.copy_pages(index=indexes),
                indexes,
                [],
            )
        ]
        entry.insert(self.type, append_entry)
        self.__journal.insert(*entry)

    def create_snapshot(self):
        entry = [("snapshot", self.copy_pages(), [], [])]
        entry.insert(self.type, [])
        self.__journal.insert(*entry)

    def change_selection(self, new_selection: list[int]):
        entry: list[_journal_entry_type] = [("selection", None, [], new_selection)]
        if self.__journal.current[1 - self.type] != entry[0]:
            entry.insert(self.type, None)
            self.__journal.insert(*entry)

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


class DocumentJournal:
    __journal: _JournalObject
    __main_journal: _JournalDocument
    __clipboard_journal: _JournalDocument

    @property
    def main(self) -> _JournalDocument:
        return self.__main_journal

    @property
    def clipboard(self) -> _JournalDocument:
        return self.__clipboard_journal

    def __init__(self, file_path: str):
        self.__journal = _JournalObject()
        self.__main_journal = _JournalDocument(self.__journal, file_path=file_path)
        self.__clipboard_journal = _JournalDocument(self.__journal)

    def duplicate_pages_in_main(self, pages: list[int]) -> fitz.Document:
        index = max(pages) + 1
        page_doc = self.__main_journal.copy_pages(pages)
        self.__main_journal.insert(index, page_doc)

        return page_doc

    def copy_pages_to_clipboard(self, pages: list[int]) -> fitz.Document:
        page_doc = self.__main_journal.copy_pages(pages)
        self.__clipboard_journal.insert(-1, page_doc)

        return page_doc

    def move_pages_to_clipboard(self, pages: list[int]) -> fitz.Document:
        page_doc = self.__main_journal.copy_pages(pages)
        self.__main_journal.delete(pages)
        last_entry = self.__journal.backward()[0]
        self.__clipboard_journal.insert(-1, page_doc, append_entry=last_entry)

        return page_doc

    def copy_pages_to_main(self, index: int, pages: list[int]) -> fitz.Document:
        page_doc = self.__clipboard_journal.copy_pages(pages)
        self.__main_journal.insert(index, page_doc)

        return page_doc

    def forward(self) -> tuple[_journal_entry_type, _journal_entry_type]:
        pass

    def backward(self) -> tuple[_journal_entry_type, _journal_entry_type]:
        pass


if __name__ == "__main__":
    journal = _JournalObject()
    journaldoc = _JournalDocument(journal)
    journaldoc.create_snapshot()
