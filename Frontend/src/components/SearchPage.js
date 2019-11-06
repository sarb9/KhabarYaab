import React, { Component } from "react";
import "./styles/SearchPage.css";
import axios from "axios";
import { withRouter } from "react-router-dom";

export class SearchPage extends Component {
  state = {
    q: "",
    redirect: false
  };

  onSubmit = e => {
    e.preventDefault();
    this.props.history.push({
      pathname: "/results",
      q: this.state.q
    });
  };

  //I could use query instead of e.target.name
  onQueryChange = e => this.setState({ [e.target.name]: e.target.value });

  render() {
    return (
      <form
        className="searchBox"
        onSubmit={this.onSubmit}
        style={{ display: "flex" }}
      >
        <input
          value={this.state.q}
          onChange={this.onQueryChange}
          name="q"
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
