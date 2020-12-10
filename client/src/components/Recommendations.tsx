import React from "react";
import { Card } from "react-bootstrap";

interface User {
  username: string;
  fullname: string;
}

interface Props {
  recommendations: User[];
}

function Recommendations(props: Props) {
  const { recommendations } = props;

  return (
    <div className="Recommendations container">
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

export default Recommendations;
