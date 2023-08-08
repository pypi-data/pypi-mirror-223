#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : vdb
# @Time         : 2023/8/7 13:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.vectorstores import DocArrayInMemorySearch as _DocArrayInMemorySearch
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import VectorStore


class DocArrayInMemorySearch(_DocArrayInMemorySearch):

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:

        docs_scores = self.similarity_search_with_score(query=query, k=k, **kwargs)

        docs = []
        for doc, score in docs_scores:
            if score > threshold:
                doc.metadata['score'] = score
                docs.append(doc)
        return docs

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[Dict[Any, Any]]] = None,
        pre_fn: Optional[Callable[[str], [str]]] = None,
        **kwargs: Any,
    ) -> VectorStore:
        """
            DocArrayInMemorySearch.from_documents(documents, embedding, pre_fn)

        """

        if pre_fn:
            texts = texts | xmap_(pre_fn)
        store = super().from_texts(texts, embedding, metadatas, **kwargs)

        return store
