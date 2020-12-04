import { User } from "../lib/types";

const search = async (tags: string[]) => {
  return await new Promise<User[]>((resolve) =>
    setTimeout(
      () =>
        resolve([
          {
            name: "Bill Gates",
            url: "https://twitter.com/BillGates",
            pic:
              "https://pbs.twimg.com/profile_images/988775660163252226/XpgonN0X_400x400.jpg",
          },
          {
            name: "Demi Lovato",
            url: "https://twitter.com/ddlovato",
            pic:
              "https://pbs.twimg.com/profile_images/1316227432194756614/o1mzNOqZ_400x400.jpg",
          },
          {
            name: "Britney Spears",
            url: "https://twitter.com/britneyspears",
            pic:
              "https://pbs.twimg.com/profile_images/1323418800876777474/0w4orMOC_400x400.jpg",
          },
        ]),
      500
    )
  );
};

export default search;
