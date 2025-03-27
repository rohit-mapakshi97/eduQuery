import eduQueryFlow from '../assets/seq_diag.png';


export const faqs = [
  {
    id: 1,
    question: "🔄 How does EduQuery answer my questions?",
    content: (
      <div>
        <p> EduQuery uses a multi-step AI pipeline to understand your question and return accurate answers from the course database. Here’s how it works:</p>

        <div style={{ textAlign: 'center' }}>
          <img
            src={eduQueryFlow}
            alt="EduQuery AI pipeline sequence"
            style={{ maxWidth: '85%', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.5)' }}
          />
        </div>
      </div>
    )
  },
  {
    id: 2,
    question: "💡 What kind of questions can EduQuery answer?",
    content: (
      <div>
        <p>EduQuery can respond to a wide range of course-related queries, organized into three main categories:</p>

        <h5>1. Engagement</h5>
        <ul>
          <li>How many students are enrolled?</li>
          <li>How many students have completed module X?</li>
          <li>How much time did students spend on module 1?</li>
          <li>How many students have completed assessment X?</li>
          <li>...and more</li>
        </ul>

        <h5>2. Performance</h5>
        <ul>
          <li>Who are the top N students for assessment X?</li>
          <li>How is student X doing?</li>
          <li>What is the average score of student X? </li>
          <li>...and more</li>
        </ul>

        <h5>3. Content & Quality</h5>
        <ul>
          <li>How did assessment X go?</li>
          <li>What did students think about the content in module X?</li>
          <li>...and more</li>
        </ul>
      </div>
    )
  },
  {
    id: 3,
    question: "🧠 Why use a Knowledge Graph instead of a SQL Database?",
    content: (
      <div>
        <p>
          While SQL databases are great for structured data and transactional queries, a knowledge graph offers unique advantages for
          complex, relationship-driven data. They benifits are outlined below:</p>
        <ul>
          <li><strong>Better representation of relationships:</strong> Courses, students, modules, and assessments are all connected. A knowledge graph models these relationships naturally and efficiently.</li>
          <li><strong>Flexible schema:</strong> Unlike rigid SQL tables, knowledge graphs allow dynamic and evolving data structures perfect for courses that change over time.</li>
          <li><strong>Faster semantic querying:</strong> Complex queries like "How is student X performing in project Y?" can be resolved faster using graph traversal instead of multiple table joins.</li>
          <li><strong>More intuitive for AI reasoning:</strong> Knowledge graphs are easier for AI systems to navigate and understand when generating Cypher queries from natural language questions.</li>
        </ul>
      </div>
    )
  },
  {
    id: 4,
    question: "🛠️ What is the tech stack used in this project?",
    content: (
      <div>
        <p>This project is built using a modern and powerful stack of technologies across the backend and frontend:</p>

        <h5>Backend</h5>
        <ul>
          <li>Python</li>
          <li>Flask</li>
          <li>LangChain</li>
          <li>Google Gemini API (LLM)</li>
          <li>Neo4j (Graph Database)</li>
        </ul>

        <h5>Frontend</h5>
        <ul>
          <li>React</li>
          <li>Bootstrap CSS</li>
        </ul>
      </div>
    )
  },
  {
    id: 5,
    question: "🧑‍💻 Can you walk me though the code?",
    content: (
      <div>
        <p>Yes! Here's a step-by-step tutorial that walks you through how this system works and how to build it yourself:</p>

        <div style={{ position: "relative", paddingBottom: "56.25%", height: 0, overflow: "hidden" }}>
          <iframe
            src="https://www.youtube.com/embed/KNvrffVhGZk?si=xanTE6Iz5g3o21zk"
            title="YouTube video player"
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%"
            }}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          ></iframe>
        </div>
      </div>

    )
  },
];
