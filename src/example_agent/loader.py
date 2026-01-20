from langchain_core.vectorstores import InMemoryVectorStore, VectorStoreRetriever


def load_rag() -> VectorStoreRetriever:
    def load_docs():
        from pathlib import Path
        from langchain_community.document_loaders import UnstructuredMarkdownLoader

        # from langchain_community.document_loaders import GitLoader

        files = ("cli_vs_gen.md", "field_helpers.md", "sql_templates.md", "workflow.md")
        p = Path("resources/gorm.io/pages/cli")

        res = []
        for f in files:
            loader = UnstructuredMarkdownLoader(
                file_path=p / f,
                # 按块加载
                # mode="elements",
            )
            # 加载文档内容
            docs = loader.load()
            res.extend(docs)
        return res

    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.embeddings import DeterministicFakeEmbedding

    docs = load_docs()
    # 按块分割
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs)
    store = InMemoryVectorStore.from_documents(
        documents=doc_splits, embedding=DeterministicFakeEmbedding(size=4096)
    )
    return store.as_retriever()
