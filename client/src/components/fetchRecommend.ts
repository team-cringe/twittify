import * as yup from "yup";
import { User } from "../lib/types";

async function fetchRecommend() {
  const res: {
    users: User[];
  } = await fetch(`/api/recommend`, {
    method: "post"
  })
    .then((res) => res.json())
    .catch((err) => alert(err.toString()));
  //   const res = {
  //     users: [
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //       {
  //         username: "Lol",
  //         fullname: "string",
  //       },
  //     ],
  //   };

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
