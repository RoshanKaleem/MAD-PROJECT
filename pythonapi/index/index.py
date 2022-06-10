from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(path=ID(stored=True), content=TEXT)
indexer = create_in("indexdir", schema)


def index_caption(caption, file_pth):
    writer = indexer.writer()
    writer.add_document(path=file_pth,
                        content=caption)
    writer.commit()


def search_caption(params):
    List = []
    with indexer.searcher() as searcher:
        query = QueryParser("content", indexer.schema).parse(params)
        results = searcher.search(query)
        for i in results:
            List.append(i['path'])
    return List
