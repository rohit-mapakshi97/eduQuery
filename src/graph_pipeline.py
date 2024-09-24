from pathlib import Path
import yaml
from typing import Dict, Any, List
from src.datamodel.graph_db import CypherQueryRepository, QueryName
from langchain_core.runnables import RunnablePassthrough
from src.pipeline.llm import LLMFactory
from src.pipeline.edu_query import EduQuery, PromptRepository, Entities
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_community.graphs import Neo4jGraph
from langchain_core.messages import AIMessage
from src.api_keys import Neo4jDBConfig
from langchain_community.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphEduQuery(EduQuery):
    """
    EduQuery pipeline which uses Neo4j database as the backend
    """

    def __init__(self) -> None:
        self.config = self._load_config()
        self.graph = self._load_graph()
        self.llm = LLMFactory().get_LLM(
            llm_provider=self.config['use_llm'],
            cfg=self.config['llm'][self.config['use_llm']]
        )
        self.prompt_repo = PromptRepository(
            prompts_file=self.config['db']['neo4j']['prompts_file']
        )
        self.query_repo = CypherQueryRepository(
            examples_file=self.config['db']['neo4j']['examples_file'],
            queries_file=self.config['db']['neo4j']['queries_file']
        )
        self.chain = None

    # Step 1: Named Entity Recognition
    def prepare_ner_chain(self):
        system, human = self.prompt_repo.get_ner_prompt()
        dict_schema = convert_to_openai_function(Entities)  # Output Format
        ner_prompt = ChatPromptTemplate.from_messages(
            [(self.SYSTEM_MESSAGE, system), (self.HUMAN_MESSAGE, human)]
        )
        entity_chain = ner_prompt | self.llm.with_structured_output(dict_schema)
        return entity_chain

    # Step 2: Matching Entities with Nodes and Relations
    def map_to_database(self, values: List[str]) -> str:
        match_query = self.query_repo.get_query(QueryName.ENTITY_DB_FULLTEXT_SEARCH)
        result = ""
        for value in values:
            response = self.graph.query(match_query, {"value": value})
            try:
                result += f"{value} maps to {response[0]['type']} node with properties: {response[0]['result']} in database\n"
            except IndexError:
                pass
        return result

    # Step 3: Prepare cypher query based on identified entities and db match
    def prepare_cypher_response(self, entity_chain):

        # 1. Few-shot Examples - pull examples from the repository
        example_prompt = ChatPromptTemplate.from_messages(
            [(self.HUMAN_MESSAGE, "{question}"), (self.SYSTEM_MESSAGE, "{query}")]
        )

        # [TODO] When the number of examples increases, migrate to SemanticSimilarityExampleSelector
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=self.query_repo.getExamples(),
            example_prompt=example_prompt,
        )

        # 2. Create Prompt
        system, human = self.prompt_repo.get_cypher_prompt()
        cypher_prompt = ChatPromptTemplate.from_messages([(self.SYSTEM_MESSAGE, system), (self.HUMAN_MESSAGE, human)])

        # 3. Prepare chain
        cypher_response = (
                RunnablePassthrough.assign(names=entity_chain)
                | RunnablePassthrough.assign(
            entities_list=lambda x: self.map_to_database(x['names'][0]['args']['names']),
            schema=lambda _: self.graph.get_schema)
                | RunnablePassthrough.assign(
            examples=lambda _: few_shot_prompt.format()
        )
                | cypher_prompt
                | self.llm.bind(stop=["\nCypherResult:"])
                | self._clean_cypher_output
        )
        return cypher_response

    # Step 4. Validate Cypher and Create Final Response
    def prepare_response_chain(self, cypher_response):
        # Cypher Validation
        corrector_schema = [
            Schema(el["start"], el["type"], el["end"])
            for el in self.graph.structured_schema.get("relationships")
        ]
        cypher_validation = CypherQueryCorrector(corrector_schema)

        # Prompt
        system, human = self.prompt_repo.get_response_prompt()
        response_prompt = ChatPromptTemplate.from_messages(
            [(self.SYSTEM_MESSAGE, system), (self.HUMAN_MESSAGE, human)]
        )

        chain = (
                RunnablePassthrough.assign(query=cypher_response)
                | RunnablePassthrough.assign(
            response=lambda x: self.graph.query(cypher_validation(x["query"])),
        )
                | response_prompt
                | self.llm
                | StrOutputParser()
        )
        return chain

    # Putting it all together
    def prepare_edu_query_chain(self):
        entity_chain = self.prepare_ner_chain()  # Step 1
        cypher_response = self.prepare_cypher_response(entity_chain)  # Step 2, 3
        edu_query_chain = self.prepare_response_chain(cypher_response)  # Step 4
        return edu_query_chain

    def ask(self, question: str, verbose: bool = False) -> str:
        # Lazy Load 
        if self.chain is None:
            self.chain = self.prepare_edu_query_chain()

        if verbose:
            self.chain.invoke({"question": question}, config={'callbacks': [ConsoleCallbackHandler()]})

        return self.chain.invoke({"question": question})

    def _load_config(self) -> Dict[str, Any]:
        llm_config_path = Path(__file__).resolve().parent.parent / 'config' / 'app_config.yaml'
        with open(llm_config_path, 'r') as file:
            return yaml.safe_load(file)

    def _load_graph(self) -> Neo4jGraph:
        return Neo4jGraph(
            url=Neo4jDBConfig.NEO4J_URI,
            username=Neo4jDBConfig.NEO4J_USER,
            password=Neo4jDBConfig.NEO4J_PASSWORD,
            database=Neo4jDBConfig.NEO4J_DATABASE
        )

    def _clean_cypher_output(self, ai_message: AIMessage) -> str:
        # Remove the ```cypher and ``` markers, and strip any extra whitespace
        clean_cypher = (ai_message.content
                        .replace("```cypher", "")
                        .replace("```", "")
                        .replace("\n", " ")
                        .strip())
        logger.info(clean_cypher)
        return clean_cypher

    # [TODO]
    # def _get_tools(self) -> List[BaseTool]:
    #     tool1 = StudentPerformanceTool(query_strategy=StudentPerformanceStrategy(self.graph))
    #     tools = [tool1]
    #     return tools

# Student Performance Tool
# class StudentPerformanceStrategy(QueryStrategy):
#     def __init__(self, graph: Neo4jGraph) -> None:
#         self.graph = graph
#
#     def get_information(self, entity: str) -> str:
#         query = CypherQueryRepository().get_query(QueryName.QA_STUDENT_PERFORMANCE)
#         try:
#             data = self.graph.query(query, params={'student_id': entity})
#             return str(data[0])
#         except IndexError:
#             return 'No information found'
