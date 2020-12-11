import React from "react";
import { Button, Card, Row } from "react-bootstrap";
import { User } from "../lib/types";
import "./Recommendations.css";

interface Props {
  recommendations: User[];
}

function Recommendations(props: Props) {
  const { recommendations } = props;

  return (
    <div className="Recommendations container d-flex">
      <Row>
        {recommendations.map((el: User, i) => (
          <Card key={i} className="user-card">
            <Card.Body>
              <Card.Title>
                {el.fullname}{" "}
                <a href={`https://twitter.com/${el.username}`}>
                  @{el.username}
                </a>
              </Card.Title>
              <Card.Text>
                Average likes: {Math.round(el.nlikes)}
                <br />
                Average replies: {Math.round(el.nreplies)}
                <br />
                Average retweets: {Math.round(el.nretweets)}
                <br />
              </Card.Text>
            </Card.Body>
          </Card>
        ))}
      </Row>
    </div>
  );
}

export default Recommendations;
