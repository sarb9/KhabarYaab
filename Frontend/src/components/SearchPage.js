import React, { Component } from "react";
import "./styles/SearchPage.css";
import { withRouter } from "react-router-dom";

export class SearchPage extends Component {
  state = {
    q: null,
    redirect: false
  };

  onSubmit = e => {
    e.preventDefault();
    if (this.props.location.pathname != "/results") {
      console.log("sending ", this.state.q);
      this.props.history.push({
        pathname: "/results",
        q: this.state.q
      });
    } else {
      this.props.onQueryChange(this.state.q);
    }
  };

  //I could use q instead of e.target.name
  onTextChange = e => this.setState({ [e.target.name]: e.target.value });

  componentDidMount() {
    if (this.props.q_history != undefined) {
      this.setState({ q: this.props.q_history });
    }
  }

  render() {
    return (
      <form
        className="searchBox"
        onSubmit={this.onSubmit}
        style={{ display: "flex" }}
      >
        <button dir="rtl" className="btn" method="Submit">
          برو !
        </button>
        <input
          dir="rtl"
          value={this.state.q}
          onChange={this.onTextChange}
          name="q"
          className="searchField"
          type="txt"
          placeholder="عبارت مدنظرتان را وارد کنید"
        ></input>
      </form>
    );
  }
}

export default withRouter(SearchPage);
