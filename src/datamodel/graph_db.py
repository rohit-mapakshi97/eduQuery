from neo4j import GraphDatabase
import logging
from pathlib import Path
from typing import List, Any, Dict
import json

logger = logging.getLogger(__name__)


class QueryName:
    """
    This class has the keys for the queries that are stored in JSON file 
    """

    # Checks
    COURSE_EXISTS = 'course_exists'
    INSTUCTOR_EXISTS = 'instructor_exists'
    STUDENT_EXISTS = 'student_exists'

    # Create Queries 
    CREATE_COURSE = 'create_course'
    CREATE_INSTRUCTOR = 'create_instructor'
    CREATE_ASSESSMENT = 'create_assessment'
    CREATE_MODULE = 'create_module'
    CREATE_STUDENT = 'create_student'
    CREATE_ENROLLEMENT = 'create_enrollment'
    CREATE_COMPLETED_ASSESSMENT = 'create_completed_assessment'
    CREATE_COMPLETED_MODULE = 'create_completed_module'

    # Create name index for DB matching
    CREATE_NAME_INDEX = 'create_name_index'

    # Clean up
    DEL_NODES_RELATIONSHIPS = 'del_nodes_relationships'
    DEL_NAME_INDEX = 'del_name_index'

    # Pipeline Queries 
    ENITY_DB_FULLTEXT_SEARCH = 'entity_db_fulltext_search'

    # @Deprecated
    # ENTITY_DB_MATCH_QUERY = 'entity_db_match_query'
    # ENTITY_DB_FUZZY_MATCH_QUERY = 'entity_db_fuzzy_match_query'
    # ENTITY_DB_APOC_NODE_SEARCH = 'entity_db_apoc_node_search'
    # ENTITY_DB_APOC_SOUNDEX_SEARCH = 'entity_db_apoc_soundex_search'


class CypherQueryRepository:
    """
    Repository for storing and managing Cypher queries for interacting with Neo4j.
    This is a Singleton Class. Which loads the stored queries into memory for access.  
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CypherQueryRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        query_folder_path = Path(__file__).resolve().parent / 'queries'
        self.examples = self._load_json(query_folder_path / 'graph_examples.json')
        self.queries = self._load_json(query_folder_path / 'graph_queries.json')

    def get_query(self, query_name: str) -> str:
        """
        Retrieve a Cypher query by name.
        """
        try:
            return self.queries[query_name]
        except KeyError:
            logger.error(f'Query: {query_name} not found in the repository.')
            raise KeyError(f'Query: {query_name} not found in the repository.')

    def getExamples(self) -> List[Dict[str, str]]:
        return self.examples

    def _load_json(self, file_path: str) -> Any:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
                # Specific exceptions should be added
        except Exception as e:
            logger.error(f'An unexpected error occurred while loading JSON from file: {file_path}')
            raise e


class Neo4jDB:
    """
    This Class is used to perform CRUD operations on Neo4j Database
    """

    def __init__(self, uri, user, password) -> None:
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            logger.error(f'Failed to initalize Neo4j DB {e}')

    def close(self):
        if self.driver:
            self.driver.close()

    # Context Management 
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def run_query(self, query, parameters=None) -> List:
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result.data()
