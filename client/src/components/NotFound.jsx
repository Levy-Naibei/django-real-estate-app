import { Container, Row, Col } from "react-bootstrap";
import { FaSadTear, FaHeartBroken } from "react-icons/fa";

const NotFound = () => {
  return (
    <Container>
      <div className="vh-100">
        <Row>
          <Col className="text-center">
            <h1 className="notfound">404</h1>
            <p>Page not found</p>
            <FaSadTear className="sad-tear" />
            <FaHeartBroken className="broken-heart" />
          </Col>
        </Row>
      </div>
    </Container>
  );
};

export default NotFound;
