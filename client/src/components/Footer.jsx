import { Container, Row, Col } from "react-bootstrap";

const Footer = () => {
  return (
    <footer className="bottom">
      <Container>
        <Row>
            <Col className="py-3">
                &copy; {new Date().getFullYear()} Real Estate. All Rights Reserved.
            </Col>
        </Row>
      </Container>
    </footer>
  )
}

export default Footer
