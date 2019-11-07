import React, { Component } from "react";
import NewsItem from "./NewsItem";
import { withRouter } from "react-router-dom";
import axios from "axios";

export class NewsFramework extends Component {
  state = {
    NewsList: [
      // {
      //   id: 1,
      //   NewsInfo: {
      //     title: "Title1",
      //     description:
      //       "شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم شبنم ",
      //     IMG:
      //       "https://image.shutterstock.com/image-photo/colorful-flower-on-dark-tropical-260nw-721703848.jpg"
      //   }
      // }
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
      .get("http://localhost:5000/search?q=" + this.props.location.q)
      .then(res => {
        console.log("here");
        console.log(res.data);
        let NewsList = [];
        res.data.news_headers.map(news => {
          news.id = 0;
          NewsList = NewsList.concat(news);
        });
        this.setState({ NewsList });
        console.log(this.state);
      })
      .catch(err => console.log(err));
  }

  render() {
    return this.state.NewsList.map(News => (
      <NewsItem key={News.id} News={News} />
    ));
  }
}

export default NewsFramework;
