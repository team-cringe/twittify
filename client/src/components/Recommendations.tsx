import React from "react";
import { Button, Card } from "react-bootstrap";
import { withRouter, RouteComponentProps } from "react-router-dom";
import { User } from "../lib/types";

interface Props {
  recommendations: User[];
}

function Recommendations(props: Props & RouteComponentProps) {
  const { recommendations, history } = props;

  return (
    <div className="Recommendations container">
      <Button variant="primary" onClick={() => history.push("/")}>
        Return to tags
      </Button>
      {recommendations.map((el, i) => (
        <Card key={i}>
          <Card.Body>
            <Card.Title>{el.fullname}</Card.Title>
            <Card.Text>{el.username}</Card.Text>
          </Card.Body>
        </Card>
      ))}
    </div>
  );
}

export default withRouter(Recommendations);
