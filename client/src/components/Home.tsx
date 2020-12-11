import React, { useEffect, useState } from "react";
import { Button, Spinner } from "react-bootstrap";
import { withRouter, RouteComponentProps } from "react-router-dom";
import { Tag } from "../lib/types";
import fetchTags from "./fetchTags";
import "./Home.css";

interface Props {
  setRecommendations: Function;
  selected: Tag[];
  setSelected: Function;
  inSelected: (tag: Tag) => number;
  ready: boolean;
  setReady: Function;
}

function Home(props: Props & RouteComponentProps) {
  console.log(process.env);
  const { history, selected, setSelected, inSelected, ready, setReady } = props;
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchTags().then((res) => {
      if (res === null || res === undefined) {
        setReady(false);
        return;
      }
      setTags(res);
      setLoading(false);
    });
  }, []);

  return ready ? (
    <div className="Home container p-5">
      <h2>Select titles that are more interesting for you</h2>

      <div className="fixed-bottom d-flex justify-content-end p-6"></div>

      {loading ? (
        <Spinner animation="border" />
      ) : (
        <div>
          {tags.map((t, i) => (
            <Button
              className="m-2"
              variant={inSelected(t) >= 0 ? "danger" : "primary"}
              key={i}
              onClick={() => {
                const ind = inSelected(t);
                console.log(ind);
                const newSelected = Array.from(selected);
                ind >= 0 ? newSelected.splice(ind, 1) : newSelected.push(t);
                console.log(newSelected);
                setSelected(newSelected);
              }}
            >
              {t.tag}
            </Button>
          ))}
        </div>
      )}
    </div>
  ) : (
    <div className="container d-flex justify-content-center">
      <h1 className="my-4">Cluster is not ready yet</h1>
    </div>
  );
}

export default withRouter(Home);
