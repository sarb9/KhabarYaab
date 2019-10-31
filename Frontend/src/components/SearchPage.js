import React, { Component } from "react";
import "./styles/SearchPage.css";
import axios from "axios";

export class SearchPage extends Component {
  state = {
    query: ""
  };

  onSubmit = e => {
    e.preventDefault();
    axios
      .post("https://jsonplaceholder.typicode.com/todos", {
        id: 1,
        NewsInfo: { title: "Title1", description: "NEWS1", IMG: "IMG1" }
      })
      .then(res => console.log(res))
      .catch(err => console.log(err));
  };

  //I could use query instead of e.target.name
  onQueryChange = e => this.setState({ [e.target.name]: e.target.value });

  render() {
    return (
      <form onSubmit={this.onSubmit} style={{ display: "flex" }}>
        <input
          value={this.state.query}
          onChange={this.onQueryChange}
          name="query"
          className="searchField"
          type="txt"
        ></input>
        <button className="btn" method="Submit">
          Go !
        </button>
      </form>
    );
  }
}

export default SearchPage;
