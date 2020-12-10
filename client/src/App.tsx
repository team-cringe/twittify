import React, { useState } from "react";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import "./App.css";
import Home from "./components/Home";
import Recommendations from "./components/Recommendations";
// import { SearchBar } from "./components/SearchBar";

interface User {
  username: string;
  fullname: string;
}

const App = () => {
  const [recommendations, setRecommendations] = useState<User[]>([]);
  const appProps = { recommendations, setRecommendations };
  return (
    <div className="App container">
      <BrowserRouter basename="/client">
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
