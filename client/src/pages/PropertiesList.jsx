import { useEffect, useState } from "react";
import { Container, Col, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";
import { fetchProperties } from "../features/properties/propertySlice";
import Spinner from "../components/Spinner";
import Property from "../components/Property";
import Title from "../components/Title";

const PropertiesList = () => {
  // const [property, setProperty ] = useState([]);
  const dispatch = useDispatch();
  const { properties, isLoading, isError, message } = useSelector(
    (state) => state.properties
  );

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }

    // setProperty(properties);

    dispatch(fetchProperties());
  }, [dispatch, isError, message]);

  // if (isLoading) {
  //   return <Spinner />;
  // }

  // console.log("property list = ", property)

  // if (isError) {
  //   return <p> Problem on our side. We will fix that ASAP </p>;
  // }

  return (
    <>
      <Container className="vh-100">
        <Title title="Properties Catalogue" />
        <Row>
          <Col className="mg-top text-center">
            <h4>Catalogue of properties</h4>
            <hr className="hr-text" />
          </Col>
        </Row>
        {isLoading ? (
          <Spinner />
        ) : (
          <>
            <Row className="mt-3">
              {properties.length &&
                properties.map((property) => (
                  <Col
                    key={property.id}
                    sm={12}
                    md={6}
                    lg={4}
                    xl={3}
                    className="m-2"
                  >
                    <Property property={property} />
                  </Col>
                ))}
            </Row>
          </>
        )}
      </Container>
    </>
  );
};

export default PropertiesList;
