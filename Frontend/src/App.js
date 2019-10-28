import React, { Component } from "react";
import NewsFramework from "./NewsFramework";
import "./App.css";
import SearchPage from "./SearchPage";

export class App extends Component {
  state = {
    NewsList: [
      {
        id: 1,
        NewsInfo: { title: "Title1", description: "NEWS1", IMG: "IMG1" }
      },
      {
        id: 2,
        NewsInfo: { title: "Title2", description: "NEWS2", IMG: "IMG2" }
      },
      {
        id: 3,
        NewsInfo: { title: "Title3", description: "NEWS3", IMG: "IMG3" }
      }
    ]
  };
  render() {
    return (
      <div className="App">
        <SearchPage />
        <NewsFramework NewsList={this.state.NewsList} />
      </div>
    );
  }
}

export default App;
