export interface User {
  username: string;
  fullname: string;
  nlikes: number;
  nreplies: number;
  nretweets: number;
}

export interface Tag {
  tag: string;
  n: number[];
}
