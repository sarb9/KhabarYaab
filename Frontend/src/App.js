import React, { Component } from "react";
import NewsFramework from "./components/NewsFramework";
import { Router, Route, Switch } from "react-router-dom";
import "./App.css";
import SearchPage from "./components/SearchPage";
import Header from "./components/Header";
import About from "./components/About";
import createHistory from "history/createBrowserHistory";

const history = createHistory();

export class App extends Component {
  render() {
    return (
      <Router history={history}>
        <Header />
        <Switch>
          <div className="container">
            <Route path="/" exact component={SearchPage} />
            <Route path="/results" component={NewsFramework} />
            <Route path="/about" component={About} />
          </div>
        </Switch>
      </Router>
    );
  }
}

export default App;
