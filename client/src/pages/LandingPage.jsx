import { Container, Button } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import Title from "../components/Title";

const LandingPage = () => {
  return (
    <header className="masthead main-bg-image">
      <Container className="h-100 d-flex align-items-center justify-content-center px-4 px-lg-5">
        <Title />
        <div className="justify-content-center">
          <div className="text-center">
            <h1 className="text-uppercase mx-auto my-0">Real Estate</h1>
            <h2 className="text-white-50 mx-auto mt-2 mb-5">
            Buy, sell or rent with us. The one stop shop for matters properties.
            </h2>
            <LinkContainer to="/properties">
              <Button variant="primary">Get Started</Button>
            </LinkContainer>
          </div>
        </div>
      </Container>
    </header>
  );
};

export default LandingPage;
