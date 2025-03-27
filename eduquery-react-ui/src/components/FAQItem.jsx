import { useState } from "react";
import { Modal, Button, ListGroup } from "react-bootstrap";

const FAQItem = ({ faq }) => {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <ListGroup.Item action onClick={handleShow}>
        {faq.question}
      </ListGroup.Item>

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>{faq.question}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{faq.content}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default FAQItem;
