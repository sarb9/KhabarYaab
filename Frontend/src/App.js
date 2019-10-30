import React, { Component } from "react";
import NewsFramework from "./components/NewsFramework";
import "./App.css";
import SearchPage from "./components/SearchPage";
import Header from "./components/Header";

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
        <Header />
        <SearchPage />
        <NewsFramework NewsList={this.state.NewsList} />
      </div>
    );
  }
}

export default App;
