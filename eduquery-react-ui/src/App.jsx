import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Button, Modal, ListGroup } from 'react-bootstrap';
import DataModelVisualization from './components/DataModelVisualization';
import { description } from './data/description.js';
import { faqs } from './data/faqs.jsx';
import './App.css';
import ChatComponent from './components/ChatComponent.jsx';
import ContactInfo from './components/ContactInfo.jsx';

function App() {
  const [show, setShow] = useState(false);
  const [currentFaq, setCurrentFaq] = useState({ question: "", content: "" });

  const handleShow = (faq) => {
    setCurrentFaq(faq);
    setShow(true);
  };

  const handleClose = () => setShow(false);

  return (
    <Container fluid className="d-flex flex-column align-items-center">
      <h1 className="display-1 fw-bold my-4" style={{ fontFamily: "'Rubik', sans-serif" }}>
        EduQuery
      </h1>
      <div>
        <p className='w-80' style={{ fontFamily: "'Rubik', sans-serif" }}>
          {description.trim().split('\n\n').map((para, i) => (
            <span className='fs-5' key={i}>
              {para}
              <br /><br />
            </span>
          ))}
        </p>
      </div>
      <Row className="flex-grow-1 text-start w-100">
        <Col md={6} className="p-4">
          {/* <h3>About</h3>
          <p>
            {description.trim().split('\n\n').map((para, i) => (
              <span key={i}>
                {para}
                <br /><br />
              </span>
            ))}
          </p> */}
          <h3>Data Model Visualization</h3>
          <DataModelVisualization />

          <h3>FAQs:</h3>
          <ListGroup style={{ maxHeight: "300px", overflowY: "auto" }}>
            {faqs.map((faq) => (
              <ListGroup.Item
                key={faq.id}
                action
                onClick={() => handleShow(faq)}
                style={{ cursor: "pointer" }}
              >
                {faq.question}
              </ListGroup.Item>
            ))}
          </ListGroup>

          <ContactInfo />

        </Col>

        <Col md={6} className="p-4" style={{ height: '80vh' }}>
          <ChatComponent />
        </Col>
      </Row>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{currentFaq.question}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{currentFaq.content}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}

export default App;
