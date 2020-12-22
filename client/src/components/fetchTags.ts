import { Tag } from "../lib/types";
import * as yup from "yup";

async function fetchTags(): Promise<Tag[] | null> {
  const res: {
    clusters: {
      tags: string[];
      n: number;
    }[];
  } | null = await fetch(`/api/tags`)
    .then((res) => (!res.ok ? null : res.json()))
    .catch((err) => alert(err.toString()));

  if (res === null) {
    return res;
  }

  const resSchema = yup.object().shape({
    clusters: yup
      .array()
      .of(
        yup.object().shape({
          tags: yup.array().of(yup.string()).required(),
          n: yup.number().required(),
        })
      )
      .required(),
  });

  const isValid = resSchema.isValidSync(res);
  if (!isValid) {
    alert(`Tags from server is not valid\n ${JSON.stringify(res, null, 2)}`);
    return Array<Tag>();
  }
  console.log(isValid);

  return res.clusters.reduce(
    (acc, el) =>
      acc.concat(
        el.tags.map((t) => {
          return { tag: t, n: [el.n] };
        })
      ),
    new Array<Tag>()
  );
}

export default fetchTags;
