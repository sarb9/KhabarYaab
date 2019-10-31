import React, { Component } from "react";
import NewsItem from "./NewsItem";

export class NewsFramework extends Component {
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
    return this.state.NewsList.map(News => (
      <NewsItem key={News.id} News={News.NewsInfo} />
    ));
  }
}

export default NewsFramework;
