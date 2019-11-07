import React, { Component } from "react";
import NewsItem from "./NewsItem";
import SearchPage from "./SearchPage";
import axios from "axios";

export class NewsFramework extends Component {
  constructor(props) {
    super(props);
    this.state = {
      NewsList: [],
      q: null,
      change_state: false
    };
  }

  componentDidMount() {
    this.setState({ q: this.props.location.q });
    console.log("heeere" + this.state.q);
    axios
      .get("http://localhost:5000/search?q=" + this.props.location.q)
      .then(res => {
        let NewsList = [];
        res.data.news_headers.map(news => {
          NewsList = NewsList.concat(news);
        });
        this.setState({ NewsList });
      })
      .catch(err => console.log(err));
  }

  componentDidUpdate() {
    if (this.state.change_state === true) {
      axios
        .get("http://localhost:5000/search?q=" + this.state.q)
        .then(res => {
          let NewsList = [];
          res.data.news_headers.map(news => {
            NewsList = NewsList.concat(news);
          });
          this.setState({ NewsList });
        })
        .catch(err => console.log(err));
      this.setState({ change_state: false });
    }
  }
  onQueryChange = new_q => {
    this.setState({ q: new_q, change_state: true });
  };

  render() {
    return (
      <div>
        <SearchPage
          onQueryChange={this.onQueryChange}
          q_history={this.state.q}
        />
        {this.state.NewsList.map(News => (
          <NewsItem key={News.id} News={News} />
        ))}
      </div>
    );
  }
}

export default NewsFramework;
