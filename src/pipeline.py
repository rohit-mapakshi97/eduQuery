from pathlib import Path
import yaml
from typing import Dict, Any, List
from datamodel.graph_db import CypherQueryRepository, QueryName
from langchain_core.runnables import RunnablePassthrough
from llm.llm_core import LLMFactory, PromptRepository
from llm.tools import Entities
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_community.graphs import Neo4jGraph
from langchain_core.messages import AIMessage
from keys import Neo4jDBConfig
from langchain_community.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain_core.output_parsers import StrOutputParser



# TODO
class EduQuery:
    def __init__(self) -> None:
        self.config = self._load_config()
        self.graph = self._load_graph()
        self.llm = LLMFactory().get_LLM(self.config)
        self.prompt_repo = PromptRepository()
        self.query_repo = CypherQueryRepository()
        self.chain = None

    # Note: The pipleine is divided into these steps to allow unit testing of individual components
    # Step 1: Named Entity Recognition
    def prepare_ner_chain(self):
        dict_schema = convert_to_openai_function(Entities)
        ner_prompt = self.prompt_repo.get_ner_prompt()
        entity_chain = ner_prompt | self.llm.with_structured_output(dict_schema)
        return entity_chain

    # Step 2: Matching Entities with Nodes and Relations
    def map_to_database(self, values: List[str]) -> str:
        # There are other options for the match query that can be tested
        match_query = self.query_repo.get_query(QueryName.ENTITY_DB_APOC_NODE_SEARCH)
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
        cypher_prompt = self.prompt_repo.get_cypher_prompt()
        cypher_response = (
                RunnablePassthrough.assign(names=entity_chain)
                | RunnablePassthrough.assign(
                    entities_list=lambda x: self.map_to_database(x['names'][0]['args']['names']),
                    schema=lambda _: self.graph.get_schema)
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
        response_prompt = self.prompt_repo.get_response_prompt()
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
        entity_chain = self.prepare_ner_chain() # Step 1
        cypher_response = self.prepare_cypher_response(entity_chain) # Step 2, 3
        edu_query_chain = self.prepare_response_chain(cypher_response) # Step 4
        return edu_query_chain

    def ask(self, question: str) -> str:
        # Lazy Load 
        if self.chain is None:
            self.chain = self.prepare_edu_query_chain()
        return self.chain.invoke({"question": question}).strip()

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
        return (ai_message.content
                .replace("```cypher", "")
                .replace("```", "")
                .replace("\n", " ")
                .strip())

if __name__ == '__main__':
    eq = EduQuery()
    while True:
        print("Enter exit to stop")
        question = input("Enter your question: ")
        if question == "exit":
            break
        resp = eq.ask(question)
        print(resp, "\n\n")
