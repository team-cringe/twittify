import { Tag } from "../lib/types";
import * as yup from "yup";

async function fetchTags(): Promise<Tag[]> {
  const res: {
    clusters: {
      tags: string[];
      n: number;
    }[];
  } = await fetch(`/api/tags`)
    .then((res) => res.json())
    .catch((err) => alert(err.toString()));
  //   const res = {
  //     clusters: [
  //       {
  //         tags: [
  //           "собаки",
  //           "собаки1",
  //           "собаки2",
  //           "собаки3",
  //           "собаки4",
  //           "собаки5",
  //           "собаки6",
  //           "собаки7",
  //           "собаки8",
  //           "собаки9",
  //         ],
  //         n: 1,
  //       },
  //       {
  //         tags: [
  //           "спорт",
  //           "спорт1",
  //           "спорт2",
  //           "спорт3",
  //           "спорт4",
  //           "спорт5",
  //           "спорт6",
  //           "спорт7",
  //           "спорт8",
  //           "спорт9",
  //           "спорт0",
  //           "спорт56",
  //           "спорт87",
  //           "спорт678",
  //           "cспорт",
  //           "cспорт1",
  //           "cспорт2",
  //           "cспорт3",
  //           "cспорт4",
  //           "cспорт5",
  //           "cспорт6",
  //           "cспорт7",
  //           "cспорт8",
  //           "cспорт9",
  //           "cспорт0",
  //           "cспорт56",
  //           "cспорт87",
  //           "cспорт678",
  //           "qспорт",
  //           "qспорт1",
  //           "qспорт2",
  //           "qспорт3",
  //           "qспорт4",
  //           "qспорт5",
  //           "qспорт6",
  //           "qспорт7",
  //           "qспорт8",
  //           "qспорт9",
  //           "qспорт0",
  //           "qспорт56",
  //           "qспорт87",
  //           "qспорт678",
  //           "qcспорт",
  //           "qcспорт1",
  //           "qcспорт2",
  //           "qcспорт3",
  //           "qcспорт4",
  //           "qcспорт5",
  //           "qcспорт6",
  //           "qcспорт7",
  //           "qcспорт8",
  //           "qcспорт9",
  //           "qcспорт0",
  //           "qcспорт56",
  //           "qcспорт87",
  //           "qcспорт678",
  //         ],
  //         n: 2,
  //       },
  //     ],
  //   };

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
          return { tag: t, n: el.n };
        })
      ),
    new Array<Tag>()
  );
}

export default fetchTags;
