import { useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import { toast } from "react-toastify";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import Title from "../components/Title";
import Spinner from "../components/Spinner";
import { activateUser, reset } from "../features/auth/authSlice";
import Footer from "../components/Footer";
import { FaCheckCircle } from "react-icons/fa";

const Activate = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { uid, token } = useParams();

  const { isLoading, isSuccess, isError, message } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }

    if (isSuccess) {
      navigate("/login");
    }
    dispatch(reset());
  }, [dispatch, isSuccess, navigate, isError, message]);

  const onSubmitHandler = (e) => {
    e.preventDefault();

    const data = { uid, token };
    dispatch(activateUser(data));
    toast.success("Your Account is now active!");
  };

  return (
    <>
      <Container className="vh-100">
        <Title title="Account Activation" />
        <Row>
          <Col className="mg-top text-center">
            <section>
              <h1>
                <FaCheckCircle /> Activate your account
              </h1>
              <hr className="hr-text" />
            </section>
          </Col>
        </Row>
        {isLoading && <Spinner />}
        <Row className="mt-3">
          <Col className="text-center">
            <Button
              className="mt-3 btn-lg"
              type="submit"
              variant="outline-success"
              onClick={onSubmitHandler}
            >
              Activate
            </Button>
          </Col>
        </Row>
      </Container>
      <Footer />
    </>
  );
};

export default Activate;
