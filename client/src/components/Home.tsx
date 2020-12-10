import React, { useEffect, useState } from "react";
import { Button, Spinner } from "react-bootstrap";
import { withRouter, RouteComponentProps } from "react-router-dom";

const serverUrl = "http://localhost:8080";

interface Tag {
  tag: string;
  n: number;
}

interface User {
  username: string;
  fullname: string;
}

async function fetchTags(): Promise<Tag[]> {
  const res: {
    clusters: {
      tags: string[];
      n: number;
    }[];
  } = await fetch(`${serverUrl}/api/tags`).then((res) => res.json());
  // const res = {
  //   clusters: [
  //     { tags: ["спорт"], n: 1 },
  //     { tags: ["собаки"], n: 2 },
  //   ],
  // };

  return res.clusters.reduce(
    (acc, el) =>
      acc.concat(
        el.tags.map((t) => {
          return { tag: t, n: el.n };
        })
      ),
    new Array<Tag>()
  );
}

async function fetchRecommend() {
  const res: {
    users: {
      username: string;
      fullname: string;
    }[];
  } = await fetch(`${serverUrl}/api/recommend`).then((res) => res.json());

  return res;
}

interface Props {
  setRecommendations: Function;
}

function Home(props: Props & RouteComponentProps) {
  console.log(props);
  const { setRecommendations, history } = props;
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selected, setSelected] = useState<Tag[]>([]);
  const [recommending, setRecommending] = useState<boolean>(false);

  const inSelected = (tag: Tag) =>
    selected.findIndex((el) => el.tag === tag.tag);

  useEffect(() => {
    fetchTags().then((res) => {
      setTags(res);
      setLoading(false);
    });
  }, []);

  return (
    <div className="Home container p-5">
      <Button
        variant="primary"
        disabled={recommending || selected.length === 0}
        onClick={async () => {
          setRecommending(true);
          await fetchRecommend().then((res) => {
            setRecommendations(res.users);
            setRecommending(false);
            console.log("push");
            history.push("/recommendations");
          });
        }}
      >
        Recommend
      </Button>
      {loading ? (
        <Spinner animation="border" />
      ) : (
        <div>
          {tags.map((t, i) => (
            <Button
              className="mx-2"
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
              #{t.tag}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
}

export default withRouter(Home);
