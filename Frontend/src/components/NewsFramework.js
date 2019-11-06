import React, { Component } from "react";
import NewsItem from "./NewsItem";
import { withRouter } from "react-router-dom";
import axios from "axios";

export class NewsFramework extends Component {
  state = {
    NewsList: [
      {
        id: 1,
        NewsInfo: {
          title: "Title1",
          description: "NEWS1",
          IMG:
            "https://image.shutterstock.com/image-photo/colorful-flower-on-dark-tropical-260nw-721703848.jpg"
        }
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

  componentDidMount() {
    // axios
    //   .get("http://localhost:5000/search?q=" + this.props.location.q)
    //   .then(res => {
    //     console.log("here");
    //     console.log(res.data);
    //     this.setState({
    //       NewsList: [res.data.news_header]
    //     });
    //     console.log(this.state);
    //   })
    //   .catch(err => console.log(err));
  }

  render() {
    return this.state.NewsList.map(News => (
      <NewsItem key={News.id} id={News.id} News={News.NewsInfo} />
    ));
  }
}

export default withRouter(NewsFramework);
