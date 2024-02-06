import { Container, Row, Col } from "react-bootstrap";

const Footer = () => {
  return (
    <footer>
      <Container>
        <Row className="text-center py-3">
            <Col>
                &copy;{new Date().getFullYear()} Real Estate. All Rights Reserved.
            </Col>
        </Row>
      </Container>
    </footer>
  )
}

export default Footer
