import React from "react";
import { Nav, Navbar, Button } from "react-bootstrap";
import { Tag, User } from "../lib/types";
import { RouteComponentProps, withRouter } from "react-router-dom";
import fetchRecommend from "./fetchRecommend";
import "./NavBar.css";

interface Props {
  selected: Tag[];
  recommending: boolean;
  setRecommending: React.Dispatch<React.SetStateAction<boolean>>;
  setRecommendations: React.Dispatch<React.SetStateAction<User[]>>;
  ready: boolean;
}

function NavBar(props: Props & RouteComponentProps) {
  const {
    selected,
    history,
    recommending,
    setRecommending,
    setRecommendations,
    ready,
  } = props;

  return (
    <Navbar bg="light" expand="lg">
      <Nav className="width-full">
        {(window.location.pathname === "/recommendations" ||
          window.location.pathname === "/client/recommendations" ||
          window.location.pathname === "/client/recommendations/") &&
          ready && (
            <Button
              className="mr-auto"
              variant="primary"
              size="lg"
              onClick={() => history.push("/")}
            >
              Return to tags
            </Button>
          )}
      </Nav>
      <Navbar.Brand>Twittify</Navbar.Brand>
      <Nav className="width-full">
        {(window.location.pathname === "/" ||
          window.location.pathname === "/client" ||
          window.location.pathname === "/client/") &&
          ready && (
            <Button
              className="recommend-btn ml-auto"
              variant={
                selected.length === 0 ? "outline-secondary" : "outline-primary"
              }
              size="lg"
              disabled={recommending || selected.length === 0}
              onClick={async () => {
                setRecommending(true);
                await fetchRecommend(selected).then((res) => {
                  setRecommendations(res);
                  setRecommending(false);
                  console.log("push");
                  history.push("/recommendations");
                });
              }}
            >
              {"Recommend ->"}
            </Button>
          )}
      </Nav>
    </Navbar>
  );
}

export default withRouter(NavBar);
