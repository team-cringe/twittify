import React, { useState } from "react";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import "./App.css";
import Home from "./components/Home";
import NavBar from "./components/NavBar";
import Recommendations from "./components/Recommendations";
// import { SearchBar } from "./components/SearchBar";
import { Tag, User } from "./lib/types";

const App = () => {
  const [recommendations, setRecommendations] = useState<User[]>([]);
  const [selected, setSelected] = useState<Tag[]>([]);
  const inSelected = (tag: Tag) =>
    selected.findIndex((el) => el.tag === tag.tag);
  const [recommending, setRecommending] = useState<boolean>(false);
  const [ready, setReady] = useState<boolean>(true);

  const appProps = {
    recommendations,
    setRecommendations,
    selected,
    setSelected,
    inSelected,
    recommending,
    setRecommending,
    ready,
    setReady,
  };
  return (
    <div className="App container">
      <BrowserRouter basename="/client">
        <NavBar {...appProps} />
        <Switch>
          <Route path="/" exact>
            <Home {...appProps} />
          </Route>
          <Route path="/recommendations" exact>
            <Recommendations {...appProps} />
          </Route>
          <Route>
            <h1>Not Found</h1>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
};

export default App;
