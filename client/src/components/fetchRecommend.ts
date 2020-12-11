import * as yup from "yup";
import { User, Tag } from "../lib/types";

async function fetchRecommend(tags: Tag[]) {
  const res: {
    users: User[];
  } = await fetch(`/api/recommend`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tags: tags }),
  })
    .then((res) => res.json())
    .catch((err) => alert(err.toString()));

  const resSchema = yup.object().shape({
    users: yup
      .array()
      .of(
        yup.object().shape({
          username: yup.string().required(),
          fullname: yup.string().required(),
        })
      )
      .required(),
  });

  const isValid = resSchema.isValidSync(res);
  if (!isValid) {
    alert(`Users from server is not valid\n ${JSON.stringify(res, null, 2)}`);
    return Array<User>();
  }

  return res.users;
}

export default fetchRecommend;
