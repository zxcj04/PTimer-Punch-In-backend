import functools
import logging
from collections import namedtuple

from .helper import hasUpdateOps

_LOGGER = logging.getLogger("connector.collection")

MongoResult = namedtuple(
    "MongoResult", ["matchedCount", "modifiedCount", "documentIds",]
)


def _assert_connection(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        assert self.collection
        return func(self, *args, **kwargs)

    return wrap


class MongoCollection(object):
    def __init__(self, mongoCollection):
        self.collection = mongoCollection

    @_assert_connection
    def insert_one(self, mDocument):
        mRet = self.collection.insert_one(mDocument)
        return MongoResult(
            matchedCount=None,
            modifiedCount=None,
            documentIds=[mRet.inserted_id] if mRet.inserted_id else [],
        )

    @_assert_connection
    def insert_many(self, mDocuments, ordered=True):
        mRet = self.collection.insert_many(mDocuments, ordered=ordered)
        return MongoResult(
            matchedCount=None, modifiedCount=None, documentIds=mRet.inserted_ids,
        )

    @_assert_connection
    def replace_one(self, mFilter, mDocument, upsert=False):
        mRet = self.collection.replace_one(mFilter, mDocument, upsert=False)
        return MongoResult(
            matchedCount=mRet.matched_count,
            modifiedCount=mRet.modified_count,
            documentIds=[mRet.upserted_id] if upsert and mRet.upserted_id else [],
        )

    @_assert_connection
    def update_one(self, mFilter, mUpdate, upsert=True):
        if not hasUpdateOps(mUpdate):
            raise MongoException.InvalidUpdateOps(mUpdate)
        mRet = self.collection.update_one(mFilter, mUpdate, upsert=upsert)
        return MongoResult(
            matchedCount=mRet.matched_count,
            modifiedCount=mRet.modified_count,
            documentIds=[mRet.upserted_id] if upsert and mRet.upserted_id else [],
        )

    @_assert_connection
    def update_many(self, mFilter, mUpdate, upsert=True):
        if not hasUpdateOps(mUpdate):
            raise MongoException.InvalidUpdateOps(mUpdate)
        mRet = self.collection.update_many(mFilter, mUpdate, upsert=upsert)
        return MongoResult(
            matchedCount=mRet.matched_count,
            modifiedCount=mRet.modified_count,
            documentIds=[mRet.upserted_id] if upsert and mRet.upserted_id else [],
        )

    @_assert_connection
    def delete_one(self, mFilter):
        if not mFilter:
            raise MongoException.InvalidDeleteOps(mFilter)
        mRet = self.collection.delete_one(mFilter)
        return MongoResult(
            matchedCount=mRet.deleted_count,
            modifiedCount=mRet.deleted_count,
            documentIds=[],
        )

    @_assert_connection
    def delete_many(self, mFilter):
        if not mFilter:
            raise MongoException.InvalidDeleteOps(mFilter)
        mRet = self.collection.delete_many(mFilter)
        return MongoResult(
            matchedCount=mRet.deleted_count,
            modifiedCount=mRet.deleted_count,
            documentIds=[],
        )

    @_assert_connection
    def aggregate(self, pipeline, cursor=False):
        c = self.collection.aggregate(pipeline)
        return [v for v in c] if not cursor else c

    @_assert_connection
    def find(self, mFilter, mProject=None, mSort=None, skip=0, limit=0, cursor=False):
        c = self.collection.find(
            mFilter, projection=mProject, sort=mSort, skip=skip, limit=limit
        )
        return [v for v in c] if not cursor else c

    @_assert_connection
    def find_one(self, mFilter, mProject=None, mSort=None, skip=0):
        return self.collection.find_one(
            mFilter, projection=mProject, sort=mSort, skip=skip
        )

    @_assert_connection
    def find_one_and_delete(self, mFilter, mProject=None, mSort=None):
        return self.collection.find_one_and_delete(
            mFilter, projection=mProject, sort=mSort
        )

    @_assert_connection
    def find_one_and_replace(
        self,
        mFilter,
        mDocument,
        mProject=None,
        mSort=None,
        upsert=False,
        returnNewDocument=False,
    ):
        return self.collection.find_one_and_replace(
            mFilter,
            mDocument,
            projection=mProject,
            sort=mSort,
            upsert=upsert,
            return_document=(
                ReturnDocument.AFTER if returnNewDocument else ReturnDocument.BEFORE
            ),
        )

    @_assert_connection
    def find_one_and_update(
        self,
        mFilter,
        mUpdate,
        mProject=None,
        mSort=None,
        upsert=False,
        returnNewDocument=True,
    ):
        if not hasUpdateOps(mUpdate):
            raise MongoException.InvalidUpdateOps(mUpdate)
        return self.collection.find_one_and_update(
            mFilter,
            mUpdate,
            projection=mProject,
            sort=mSort,
            upsert=upsert,
            return_document=(
                ReturnDocument.AFTER if returnNewDocument else ReturnDocument.BEFORE
            ),
        )

    @_assert_connection
    def count_documents(self, mFilter, skip=0, limit=0):
        return self.collection.count_documents(mFilter, skip=skip, limit=limit)

    @_assert_connection
    def estimated_document_count(self, **kwargs):
        return self.collection.estimated_document_count(**kwargs)
