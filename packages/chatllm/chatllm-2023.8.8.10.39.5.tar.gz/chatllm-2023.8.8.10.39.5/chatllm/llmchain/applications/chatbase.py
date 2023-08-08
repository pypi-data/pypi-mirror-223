#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatdoc
# @Time         : 2023/7/15 20:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from chatllm.llmchain.utils import docs2dataframe
from chatllm.llmchain.decorators import llm_stream
from chatllm.llmchain.vectorstores import Milvus
from chatllm.llmchain.embeddings import OpenAIEmbeddings, DashScopeEmbeddings
from chatllm.llmchain.document_loaders import FilesLoader
from chatllm.llmchain.prompts.prompt_templates import context_prompt_template

from langchain.text_splitter import *
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.base import Embeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseLanguageModel
from langchain.vectorstores import VectorStore


class ChatBase(object):

    def __init__(self,
                 llm: BaseLanguageModel = ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0, streaming=True),
                 embeddings: Embeddings = OpenAIEmbeddings(chunk_size=5),

                 vectorstore: Optional[VectorStore] = None,

                 collection_name: str = 'TEST',  # todo: 重构

                 get_api_key: Optional[Callable[[int], List[str]]] = None,
                 prompt_template=context_prompt_template,
                 ):
        """

        :param llm:
        :param embeddings:
        :param collection_name:
        :param get_api_key:
        :param prompt_template:
        """
        self.collection_name = collection_name
        self.llm = llm
        self.embeddings = embeddings

        self.prompt_template = prompt_template  # cb.chain.llm_chain.prompt.messages

        if get_api_key:
            self.embeddings.get_api_key = get_api_key
            self.embeddings.openai_api_key = get_api_key(1)[0]
            self.llm.openai_api_key = get_api_key(1)[0]

        self.chain = load_qa_chain(
            self.llm,
            chain_type="stuff",
            prompt=ChatPromptTemplate.from_template(prompt_template)  # todo: 增加上下文信息
        )

        _vdb_kwargs = self.vdb_kwargs.copy()
        _vdb_kwargs['embedding_function'] = _vdb_kwargs.pop('embedding')  # 参数一致性
        # _vdb_kwargs['drop_old'] = True # 重新创建
        self.vectorstore: Optional[Milvus] = vectorstore or Milvus(**_vdb_kwargs)

    def pipeline(self):
        pass

    def llm_qa(self, query: str, k: int = 5, threshold: float = 0.5, **kwargs: Any):
        """todo: pipeline"""
        docs = self.vectorstore.similarity_search(query, k=max(k, 10), threshold=threshold, **kwargs)
        docs = docs | xUnique_plus(lambda doc: doc.page_content.strip())  # 按内容去重，todo: 按语义相似度去重
        docs = docs[:k]
        if docs:
            # chain.run(input_documents=docs, question=query)
            return llm_stream(self.chain.run)({"input_documents": docs, "question": query})

    @staticmethod
    def load_file(file_paths, chunk_size=2000, chunk_overlap=200, **kwargs):
        """支持多文件"""
        loader = FilesLoader(file_paths)
        docs = loader.load_and_split(
            RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)
        )
        return docs

    # @diskcache(location=os.getenv('INSERT_VECTOR_CACHE', '~/.cache/insert_vector_cache'), ignore=['self'])
    def create_index(self, docs: List[Document], **kwargs):
        """初始化 drop_old=True"""
        self.vectorstore = Milvus.from_documents(docs, **{**self.vdb_kwargs, **kwargs})

    @property
    def vdb_kwargs(self):
        connection_args = {
            'uri': os.getenv('ZILLIZ_ENDPOINT'),
            'token': os.getenv('ZILLIZ_TOKEN')
        }
        address = os.getenv('MILVUS_ADDRESS')  # 该参数优先
        if address:
            connection_args.pop('uri')
            connection_args['address'] = address

        index_params = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }

        embedding_function = self.embeddings

        vdb_kwargs = dict(
            embedding=embedding_function,
            connection_args=connection_args,
            index_params=index_params,
            search_params=None,
            collection_name=self.collection_name,
            drop_old=False,
        )

        return vdb_kwargs
