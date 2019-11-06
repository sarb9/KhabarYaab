import React, { Component } from "react";
import NewsItem from "./NewsItem";
import axios from "axios";

export class NewsFramework extends Component {
  state = {
    NewsList: [
      // {
      //   id: 1,
      //   NewsInfo: { title: "Title1", description: "NEWS1", IMG: "IMG1" }
      // },
      // {
      //   id: 2,
      //   NewsInfo: { title: "Title2", description: "NEWS2", IMG: "IMG2" }
      // },
      // {
      //   id: 3,
      //   NewsInfo: { title: "Title3", description: "NEWS3", IMG: "IMG3" }
      // }
    ]
  };

  componentDidMount() {
    axios
      .get("https://jsonplaceholder.typicode.com/todos?_limit=10")
      .then(res => console.log(res.data));
    this.setState({
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
    });
  }

  render() {
    console.log(this.state);
    return this.state.NewsList.map(News => (
      <NewsItem key={News.id} News={News.NewsInfo} />
    ));
  }
}

export default NewsFramework;
