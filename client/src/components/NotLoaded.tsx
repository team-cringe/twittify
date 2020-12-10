import React from "react";

interface Props {}

function NotLoaded(props: Props) {
  const {} = props;

  return (
    <div className="NotLoaded container d-flex justify-content-center my-6">
      <h1>Clustering not complete</h1>
    </div>
  );
}

export default NotLoaded;
