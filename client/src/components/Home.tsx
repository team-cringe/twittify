import React, { useEffect, useState } from "react";
import { Button, Spinner } from "react-bootstrap";
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

function Home(props: Props) {
  const { selected, setSelected, inSelected, ready, setReady } = props;
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchTags().then((res) => {
      if (res === null || res === undefined) {
        setReady(false);
        return;
      }

      const tags = res.reduce((acc, v) => {
        let elToAdd: Tag;
        console.log("acc", acc);
        if (acc.has(v.tag)) {
          elToAdd = acc.get(v.tag) || v;
          elToAdd.n = elToAdd!.n.concat(v.n);
        } else {
          elToAdd = v;
        }
        acc.set(elToAdd!.tag, elToAdd);

        return acc;
      }, new Map<string, Tag>());

      setTags(Array.from(tags.values()));
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

export default Home;
