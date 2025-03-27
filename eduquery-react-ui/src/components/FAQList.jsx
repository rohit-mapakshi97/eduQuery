import FAQItem from "./FAQItem";
import { ListGroup } from "react-bootstrap";

const FAQList = ({ faqs }) => (
  <ListGroup style={{ maxHeight: "300px", overflowY: "auto" }}>
    {faqs.map((faq) => (
      <FAQItem key={faq.id} faq={faq} />
    ))}
  </ListGroup>
);

export default FAQList;
