import React, { useEffect, useState } from "react";
import { Button, Spinner } from "react-bootstrap";
import { withRouter, RouteComponentProps } from "react-router-dom";
import { Tag } from "../lib/types";
import fetchTags from "./fetchTags";
import fetchRecommend from "./fetchRecommend";
import "./Home.css";

interface Props {
  setRecommendations: Function;
}

function Home(props: Props & RouteComponentProps) {
  console.log(process.env);
  const { setRecommendations, history } = props;
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selected, setSelected] = useState<Tag[]>([]);
  const [recommending, setRecommending] = useState<boolean>(false);

  const inSelected = (tag: Tag) =>
    selected.findIndex((el) => el.tag === tag.tag);

  useEffect(() => {
    fetchTags().then((res) => {
      if (res === null || res === undefined) {
        history.push("/not-loaded");
        return;
      }
      setTags(res);
      setLoading(false);
    });
  }, []);

  return (
    <div className="Home container p-5">
      <h2>Select titles that are more interesting for you</h2>

      <div className="fixed-bottom d-flex justify-content-end p-6">
        <Button
          className="recommend-btn"
          variant={
            selected.length === 0 ? "outline-secondary" : "outline-primary"
          }
          size="lg"
          disabled={recommending || selected.length === 0}
          onClick={async () => {
            setRecommending(true);
            await fetchRecommend().then((res) => {
              setRecommendations(res);
              setRecommending(false);
              console.log("push");
              history.push("/recommendations");
            });
          }}
        >
          {"Recommend ->"}
        </Button>
      </div>

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
  );
}

export default withRouter(Home);
