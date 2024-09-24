import yaml

from src.datamodel.graph_db import Neo4jDB, CypherQueryRepository, QueryName
from pathlib import Path
import csv
from src.api_keys import Neo4jDBConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# This script is used to load all courses in ./data folder into Neo4j DB
# Opted for a functional approach than a single LOAD query so I can add any file-specific preprocessing if needed 

def process_course_folder(course_folder: Path, db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    folder_name = course_folder.name
    course_id, semester, section_number = folder_name.split('_')

    # 1. Create course node. Skip if course already procesed.
    if is_course_created(course_id, semester, section_number, db, query_repo):
        logger.info(
            f'Course {course_id} for {semester} section {section_number} already exists. Skipping...')
        return
    create_course_node(course_id, semester, section_number, db, query_repo)

    # 2. Add Instructor Node
    instructors_file = course_folder / 'instructor.csv'
    create_instructor_node(instructors_file, course_id,
                           semester, section_number, db, query_repo)

    # 3. Add Student Nodes
    # Here we also create an extra relationship called ENROLLED to query faster
    students_file = course_folder / 'students.csv'
    create_student_node(students_file, course_id, db, query_repo)

    # 4. Add Assessment Nodes
    assessments_file = course_folder / 'assessments.csv'
    create_assessment_node(assessments_file, course_id, db, query_repo)

    # 5. Add Module Nodes
    modules_file = course_folder / 'modules.csv'
    create_module_node(modules_file, course_id, db, query_repo)

    # 6. Add Assessment Completion Edges
    assessment_completions_file = course_folder / \
                                  'student_assessment_completions.csv'
    create_completed_assessment_relation(
        assessment_completions_file, db, query_repo)

    # 7. Add Module Completion Edges
    module_completions_file = course_folder / 'student_module_completions.tsv'
    create_completed_module_relation(module_completions_file, db, query_repo)

    # 8. Create nameIndex for DB matching Entities
    create_name_index(db, query_repo)


def is_course_created(course_id: str, semester: str, section_number: str, db: Neo4jDB,
                      query_repo: CypherQueryRepository) -> bool:
    result = db.run_query(query_repo.get_query(QueryName.COURSE_EXISTS), {
        "course_id": course_id,
        "semester": semester,
        "section_number": section_number
    })
    return len(result) > 0


def create_course_node(course_id: str, semester: str, section_number: str, db: Neo4jDB,
                       query_repo: CypherQueryRepository) -> None:
    db.run_query(query_repo.get_query(QueryName.CREATE_COURSE), {
        "course_id": course_id,
        "semester": semester,
        "section_number": section_number
    })


def create_instructor_node(file: Path, course_id: str, semester: str, section_number: str, db: Neo4jDB,
                           query_repo: CypherQueryRepository) -> None:
    def is_instructor_exist(instructor_id):
        result = db.run_query(query_repo.get_query(QueryName.INSTRUCTOR_EXISTS), {
            "instructor_id": instructor_id})
        return len(result) > 0

    if file.exists():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if is_instructor_exist(row["instructor_id"]):
                    logger.info(
                        f'Instructor {row["instructor_id"]} already exists ans skipped')
                    continue  # skip

                db.run_query(query_repo.get_query(QueryName.CREATE_INSTRUCTOR), {
                    "instructor_id": row["instructor_id"],
                    "instructor_name": row["instructor_name"],
                    "course_id": course_id,
                    "semester": semester,
                    "section_number": section_number
                })
        logger.info('Added Instructors')


def create_student_node(file: Path, course_id: str, db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    def is_student_exists(student_id) -> bool:
        result = db.run_query(query_repo.get_query(QueryName.STUDENT_EXISTS), {
            "student_id": student_id})
        return len(result) > 0

    if file.exists():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if is_student_exists(row['student_id']):
                    logger.info(
                        f'Student {row["student_id"]} already exists, skipping node creation. But will be enrolled')
                else:
                    db.run_query(query_repo.get_query(QueryName.CREATE_STUDENT), {
                        "student_id": row['student_id'],
                        "student_name": row['name']
                    })

                db.run_query(query_repo.get_query(QueryName.CREATE_ENROLMENT), {
                    "student_id": row['student_id'],
                    "course_id": course_id
                })
        logger.info('Added Students')


def create_module_node(file: Path, course_id: str, db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    if file.exists():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.run_query(query_repo.get_query(QueryName.CREATE_MODULE), {
                    "module_id": row['module_id'],
                    "module_name": row['module_name'],
                    "course_id": course_id
                })
        logger.info('Added Modules')


def create_assessment_node(file: Path, course_id: str, db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    if file.exists():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.run_query(query_repo.get_query(QueryName.CREATE_ASSESSMENT), {
                    "assessment_id": row['assessment_id'],
                    "assessment_name": row['assessment_name'],
                    "course_id": course_id
                })
        logger.info('Added Assessments')


def create_completed_assessment_relation(file: Path, db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    if file.exists():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.run_query(query_repo.get_query(QueryName.CREATE_COMPLETED_ASSESSMENT), {
                    "completion_id": row['completion_id'],
                    "assessment_id": row['assessment_id'],
                    "student_id": row['student_id'],
                    "score": row['score'],
                    "attempts": row['attempts']
                })
        logger.info('Added Assignment Submissions')


def create_completed_module_relation(file: Path, db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    if file.exists():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                db.run_query(query_repo.get_query(QueryName.CREATE_COMPLETED_MODULE), {
                    "completion_id": row['completion_id'],
                    "student_id": row['student_id'],
                    "module_id": row['module_id'],
                    "minutes_spent": row['minutes_spent'],
                    "feedback": row['feedback'],
                    "rating": row['rating']
                })
        logger.info('Added Module Completions')


def create_name_index(db: Neo4jDB, query_repo: CypherQueryRepository) -> None:
    db.run_query(query_repo.get_query(QueryName.CREATE_NAME_INDEX))
    logger.info('Created Name Index')


def clean_up() -> None:
    root_folder = Path(__file__).resolve().parent.parent

    with open(root_folder / 'config'/ 'app_config.yaml') as file:
        config = yaml.safe_load(file)

    query_repo = CypherQueryRepository(
        examples_file=config['db']['neo4j']['examples_file'],
        queries_file=config['db']['neo4j']['queries_file']
    )

    with Neo4jDB(Neo4jDBConfig.NEO4J_URI, Neo4jDBConfig.NEO4J_USER, Neo4jDBConfig.NEO4J_PASSWORD) as db:

        # 1. Delete Name index
        db.run_query(query_repo.get_query(QueryName.DEL_NAME_INDEX))
        logger.info('Deleted Name Index')

        # 2. Delete Nodes and relationships
        db.run_query(query_repo.get_query(QueryName.DEL_NODES_RELATIONSHIPS))
        logger.info('Dropped all nodes and relationships')


def setup_db():
    root_folder = Path(__file__).resolve().parent.parent

    with open(root_folder / 'config'/ 'app_config.yaml') as file:
        config = yaml.safe_load(file)
    # 1. Initialize Database
    with Neo4jDB(Neo4jDBConfig.NEO4J_URI, Neo4jDBConfig.NEO4J_USER, Neo4jDBConfig.NEO4J_PASSWORD) as db:
        query_repo = CypherQueryRepository(
            examples_file=config['db']['neo4j']['examples_file'],
            queries_file=config['db']['neo4j']['queries_file']
        )
        # 2. Populate data from CSV Files
        courses_folder = root_folder / 'data'

        for course_folder in courses_folder.iterdir():
            if course_folder.is_dir():
                try:
                    logger.info(
                        f'Processing course folder: {course_folder.name}')
                    process_course_folder(course_folder, db, query_repo)
                except Exception as e:
                    logger.warning(
                        f'Exception occurred while creating KG for {course_folder.name}')
                    raise e
            else:
                logger.info(f'Skipping non-directory item: {course_folder}')


if __name__ == '__main__':
    print("Select one of the options below (1 or 2):\n",
          "\t 1. Clean up database\n",
          "\t 2. Setup database\n"
          )
    choice = input("Your option: ")
    if choice == "1":
        clean_up()
    else:
        setup_db()


