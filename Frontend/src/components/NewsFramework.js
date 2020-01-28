import React, { Component } from "react";
import moment from "moment";
import NewsItem from "./NewsItem";
import SearchPage from "./SearchPage";
import axios from "axios";

export class NewsFramework extends Component {
  constructor(props) {
    super(props);
    this.state = {
      NewsList: [],
      q: null,
      change_state: false,
      sort_value: "relevance",
      NewsListRelevance: [],
      NewsListTime: []
    };
  }

  componentDidMount() {
    this.setState({ q: this.props.location.q });
    axios
      .get("http://localhost:5000/search?q=" + this.props.location.q)
      .then(res => {
        let NewsList = [];
        res.data.news_headers.map(news => {
          NewsList = NewsList.concat(news);
        });
        this.setState({ NewsList });
        this.setState({ NewsListRelevance: NewsList });
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
          this.setState({ NewsListRelevance: NewsList });
        })
        .catch(err => console.log(err));
      this.setState({ change_state: false });
    }
  }
  onQueryChange = new_q => {
    this.setState({ q: new_q, change_state: true });
  };

  onSortChange = e => {
    console.log(e.target.value);
    this.setState({ sort_value: e.target.value });
    console.log("here", this.state);
    let NewsList = this.state.NewsList;
    if (this.state.sort_value == "time") {
      if (this.state.NewsListTime.length == 0) {
        for (let i = 0; i < NewsList.length - 1; i++) {
          for (let j = 0; j < NewsList.length - 1; j++) {
            if (
              this.compareDates(
                NewsList[j + 1].publish_date,
                NewsList[j].publish_date
              ) == 1
            ) {
              console.log(NewsList);
              let tmp = NewsList[j];
              NewsList[j] = NewsList[j + 1];
              NewsList[j + 1] = tmp;
              console.log(NewsList);
            }
          }
        }
        this.setState({ NewsListTime: NewsList });
        this.setState({ NewsList: NewsList });
      } else {
        this.setState({ NewsList: this.state.NewsListTime });
      }
    } else {
      this.setState({ NewsList: this.state.NewsListRelevance });
    }
  };

  compareDates(dateTimeA, dateTimeB) {
    let momentA = moment(dateTimeA, "MMMM Do YYYY, h:mm:ss");
    let momentB = moment(dateTimeB, "MMMM Do YYYY, h:mm:ss");
    if (momentA > momentB) {
      console.log("hereeeeeee " + momentA + " " + momentB);
      return 1;
    } else return 0;
  }

  render() {
    return (
      <div>
        <SearchPage
          onQueryChange={this.onQueryChange}
          q_history={this.state.q}
        />
        <label style={sortParentStyle}>
          Sort By:
          <select
            value={this.state.sort_value}
            onChange={this.onSortChange}
            style={sortStyle}
          >
            <option
              value="relevance"
              selected={this.state.sort_value == "relevance"}
            >
              relevance
            </option>
            <option value="time" selected={this.state.sort_value == "time"}>
              time
            </option>
          </select>
        </label>
        {this.state.NewsList.map(News => (
          <NewsItem key={News.id} News={News} />
        ))}
      </div>
    );
  }
}

export default NewsFramework;

const sortParentStyle = {
  width: "100%"
};
const sortStyle = {
  color: "red",
  width: "90%",
  marginLeft: "2%",
  fontWeight: "bold"
};
