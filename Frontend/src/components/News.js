import React, { Component } from "react";

export default class News extends Component {
  state = {
    News: []
  };
  componentWillMount() {
    //getNewsById
  }
  render() {
    return <div>{this.state.News}</div>;
  }
}
