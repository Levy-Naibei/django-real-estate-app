import { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form } from "react-bootstrap";
import { toast } from "react-toastify";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { FaUserPlus } from "react-icons/fa";
import Title from "../components/Title";
import Spinner from "../components/Spinner";
import Footer from "../components/Footer";
import { register, reset } from "../features/auth/authSlice";

function Signup() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [re_password, setRepassword] = useState("");

  const { isLoading, isError, isSuccess, message, user } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }
    if (isSuccess || user) {
      navigate("/activate/:uid/:token");
      toast.success("Activation link sent to your email.")
    }
    dispatch(reset());
  }, [isError, isSuccess, message, navigate, dispatch, user]);

  const onSubmitHandler = (e) => {
    e.preventDefault();

    if (!username) {
      toast.error("Username must be provided!");
    }

    if (!first_name) {
      toast.error("Fist name must be provided!");
    }

    if (!last_name) {
      toast.error("Last name must be provided!");
    }

    if (!email) {
      toast.error("Email must be provided!");
    }

    if (!password) {
      toast.error("Password must be provided!");
    }

    if (!re_password) {
      toast.error("Password must be provided!");
    }

    if (password !== re_password) {
      toast.error("Password mismatch!");
    }

    const data = { username, first_name, last_name, email, password, re_password };
    dispatch(register(data));
  };

  return (
    <>
      <Container>
        <Title title="Sign Up" />
        <Row>
          <Col className="mg-top text-center">
            <section>
              <h1>
                <FaUserPlus /> Register
              </h1>
              <hr className="hr-text" />
            </section>
          </Col>
        </Row>
        {isLoading && <Spinner />}
        <Row className="mt-3">
          <Col className="justify-content-center">
            <Form onSubmit={onSubmitHandler}>
              <Form.Group className="mt-3" controlId="username">
                {/* <Form.Label>Username</Form.Label> */}
                <Form.Control
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mt-3" controlId="first_name">
                {/* <Form.Label>First Name</Form.Label> */}
                <Form.Control
                  type="text"
                  placeholder="First Name"
                  value={first_name}
                  onChange={(e) => setFirstName(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mt-3" controlId="last_name">
                {/* <Form.Label>Last Name</Form.Label> */}
                <Form.Control
                  type="text"
                  placeholder="Last Name"
                  value={last_name}
                  onChange={(e) => setLastName(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mt-3" controlId="email">
                {/* <Form.Label>Email</Form.Label> */}
                <Form.Control
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mt-3" controlId="password">
                {/* <Form.Label>Password</Form.Label> */}
                <Form.Control
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mt-3" controlId="re_password">
                {/* <Form.Label>Password</Form.Label> */}
                <Form.Control
                  type="password"
                  placeholder="Confirm Password"
                  value={re_password}
                  onChange={(e) => setRepassword(e.target.value)}
                />
              </Form.Group>
              <Button
                className="mt-3"
                type="submit"
                variant="primary"
                // onClick={isLoading? <Spinner /> : "Login"}
              >
                Signup
              </Button>
            </Form>
          </Col>
        </Row>
        <Row className="py-3">
          <Col className="d-flex justify-content-center">
            Have an account?{" "}
            <Link className="auth-link" to="/login">
              Log in
            </Link>
          </Col>
        </Row>
      </Container>
      <Footer />
    </>
  );
}

export default Signup;
