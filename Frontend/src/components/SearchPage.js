import React, { Component } from "react";
import "./styles/SearchPage.css";
import { Redirect } from "react-router";
import axios from "axios";

export class SearchPage extends Component {
  state = {
    q: "",
    redirect: false
  };

  onSubmit = e => {
    e.preventDefault();
    axios
      .post("https://jsonplaceholder.typicode.com/todos", {
        id: 1,
        NewsInfo: { title: "Title1", description: "NEWS1", IMG: "IMG1" }
      })
      .then(res => {
        console.log(res);
        this.setState({ redirect: true });
      })
      .catch(err => console.log(err));
  };

  //I could use query instead of e.target.name
  onQueryChange = e => this.setState({ [e.target.name]: e.target.value });

  render() {
    return this.state.redirect ? (
      <Redirect
        to={{
          pathname: "/results",
          state: { id: "123" }
        }}
      />
    ) : (
      <form onSubmit={this.onSubmit} style={{ display: "flex" }}>
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
