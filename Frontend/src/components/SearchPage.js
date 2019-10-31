import React, { Component } from "react";
import "./styles/SearchPage.css";

export class SearchPage extends Component {
  state = {
    query: ""
  };

  onSubmit = e => {
    e.preventDefault();
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
