from arango import ArangoClient
import time


class FerhassioSaver:
    """
    Customized ArangoDB connector. Can create Databases and Collections.
    """

    def __init__(self, hosts, user, password, dbname, coll):
        """
        Create new connection to ArangoDB base and collection
        :param dbname: Database name
        :type dbname: str, list
        :param coll: Collection name
        :type coll:str
        """
        self.client = ArangoClient(hosts=hosts)
        self.database = self.client.db(dbname, username=user, password=password)
        self.async_db = self.database.begin_async_execution()
        self.async_coll = self.async_db.collection(coll)
        self.coll_name = coll
        self.async_aql = self.async_db.aql
        self.time_spent = 0
        self.workers_count = 0

    def create_unique_field(self, field: str):
        """
        Create unique index in document
        :param field: Key name
        :return: Creation state
        """
        return self.async_coll.add_hash_index(fields=[str(field)], unique=True)  # Creating unique key

    def fetch_data(self, cnt=None, field=None) -> list:
        """
        Fetch docs from Arango using AQL 'RETURN' method like [FIFO]
        :param field: Filter to show current value from doc (optional)
        :param cnt: How many docs need to fetch
        :type cnt: int
        :return: Fetched data
        """
        self.time_spent = 0

        transaction_start_time = time.time()

        if cnt:
            job = self.database.aql.execute(f"FOR doc IN {self.async_coll.name} LIMIT {cnt} SORT doc._key ASC RETURN doc{'.'+ field if field else ''}")

        else:
            job = self.database.aql.execute(f"FOR doc IN {self.async_coll.name} RETURN doc{'.'+ field if field else ''}")

        fetched_data = [document for document in job]

        transaction_end_time = time.time()

        self.time_spent += round(transaction_end_time - transaction_start_time, 5)

        return fetched_data

    def fetch_by(self, by_field, value):
        """
        Fetch data using field and value like (_key, 123456).
        :param by_field: Filtered document field (key).
        :param value: Document value
        :return: Filtered results
        """
        if by_field and value:
            job = self.database.aql.execute(f"FOR doc IN {self.async_coll.name} FILTER doc.{by_field} == '{value}' "
                                            f"RETURN doc")
            fetched_data = [document for document in job]
        else:
            raise AttributeError

        return fetched_data

    def load_data(self, json_list: list, chunk_size: int, on_duplicate: str = 'replace', overwrite: bool = False) -> None:
        """
        Save to ArangoDB
        :param chunk_size: Chunk size for worker
        :param json_list: List of jsons from page
        :param overwrite: Overwrite data in dab or not
        :param on_duplicate: replace(default), update, ignore
        :return: None
        """
        self.workers_count = 0
        self.time_spent = 0

        transaction_start_time = time.time()

        chunk_generator = [json_list[i:i + chunk_size] for i in range(0, len(json_list), chunk_size)]

        for chunk in chunk_generator:
            self.async_coll.import_bulk(chunk, on_duplicate=on_duplicate, overwrite=overwrite)
            self.workers_count += 1

        transaction_end_time = time.time()
        self.time_spent += round(transaction_end_time - transaction_start_time, 5)

    def load_once(self, doc: dict, overwrite_mode='update') -> None:
        """
        Load one document
        :param doc: json
        :param overwrite_mode: update(default), replace
        :return: None
        """
        self.async_coll.insert(doc, overwrite_mode=overwrite_mode)

    def is_valid(self, doc):
        """
        Check if document in DB
        :param doc: json
        :return: True if in database, else False
        """
        return self.database.has_document(doc)

    def delete(self, doc: dict):
        return self.database.delete_document(doc)

    def execute(self, aql: str) -> list:
        """
        Execute AQL query
        :param aql: Query
        :return: Result
        """
        return [document for document in self.database.aql.execute(aql)]

    def collection_count(self) -> int:
        """
        Get element count in selected connected collection
        :return: Elements count
        """
        return self.database.collection(self.coll_name).count()
