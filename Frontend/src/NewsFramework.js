import React, { Component } from "react";
import NewsItem from "./NewsItem";

export class NewsFramework extends Component {
  render() {
    return this.props.NewsList.map(News => (
      <NewsItem key={News.id} News={News.NewsInfo} />
    ));
  }
}

export default NewsFramework;
