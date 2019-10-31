import React, { Component } from "react";
import NewsFramework from "./components/NewsFramework";
import { BrowserRouter as Router, Route } from "react-router-dom";
import "./App.css";
import SearchPage from "./components/SearchPage";
import Header from "./components/Header";

export class App extends Component {
  render() {
    return (
      <Router>
        <div className="container">
          <Header />
          <Route
            path="/"
            render={props => (
              <React.Fragment>
                <SearchPage />
              </React.Fragment>
            )}
          />
          <Route path="/Results" render={props => <NewsFramework />} />
        </div>
      </Router>
    );
  }
}

export default App;
