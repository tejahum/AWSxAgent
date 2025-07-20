from pymongo.database import Database
from typing import Any, List, Dict

def insert_document(db: Database, collection_name: str, document: Dict[str, Any]) -> Any:
    """
    Inserts a single document into the specified collection.
    Returns the inserted document's _id.
    Raises ConnectionError if insertion fails.
    """
    try:
        result = db[collection_name].insert_one(document)
        return result.inserted_id
    except Exception as e:
        raise ConnectionError(f"Failed to insert document into '{collection_name}': {e}")

def insert_documents(db: Database, collection_name: str, documents: List[Dict[str, Any]]) -> List[Any]:
    """
    Inserts multiple documents into the specified collection.
    Returns a list of inserted_ids.
    Raises ConnectionError if insertion fails.
    """
    try:
        result = db[collection_name].insert_many(documents)
        return result.inserted_ids
    except Exception as e:
        raise ConnectionError(f"Failed to insert documents into '{collection_name}': {e}")

def find_documents(
    db: Database,
    collection_name: str,
    query: Dict[str, Any] = None,
    limit: int = 0
) -> List[Dict[str, Any]]:
    """
    Retrieves documents matching `query` from the specified collection.
    - query: Mongo filter dict (defaults to {} for all documents)
    - limit: max number of documents to return (0 means no limit)
    Returns a list of document dicts.
    Raises ConnectionError on failure.
    """
    try:
        cursor = db[collection_name].find(query or {})
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)
    except Exception as e:
        raise ConnectionError(f"Failed to retrieve documents from '{collection_name}': {e}")
