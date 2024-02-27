import { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form } from "react-bootstrap";
import { toast } from "react-toastify";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { FaSignInAlt } from "react-icons/fa";
import Title from "../components/Title";
import Spinner from "../components/Spinner";
import { login, reset } from "../features/auth/authSlice";

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { isLoading, isSuccess, isError, message, user } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }

    if (isSuccess || user) {
      navigate("/");
    }
    dispatch(reset());
  }, [user, dispatch, isSuccess, navigate, isError, message]);

  const handleLogin = (e) => {
    e.preventDefault();

    if (!email) {
      toast.error("Email must be provided!");
    }

    if (!password) {
      toast.error("Password must be provided!");
    }

    const data = { email, password };
    return dispatch(login(data));
  };

  // const handleOnLoginChange = () => {

  // }

  return (
    <>
      <Container className="vh-100">
        <Title title="Login" />
        <Row>
          <Col className="mg-top text-center">
            <section>
              <h1>
                <FaSignInAlt /> Login
              </h1>
              <hr className="hr-text" />
            </section>
          </Col>
        </Row>
        {isLoading && <Spinner />}
        <Row className="mt-3">
          <Col className="d-flex justify-content-center">
            <Form onSubmit={handleLogin}>
              <Form.Group className="mt-3" controlId="email">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mt-3" controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </Form.Group>
              <Button
                className="mt-3"
                type="submit"
                variant="primary"
                // onClick={isLoading? <Spinner /> : "Login"}
              >
                Login
              </Button>
            </Form>
          </Col>
        </Row>
        <Row className="py-3">
          <Col className="d-flex justify-content-center">
            Don't have an account? <Link className="auth-link" to="/register">Sign up</Link>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Login;
