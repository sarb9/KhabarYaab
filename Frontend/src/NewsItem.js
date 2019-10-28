import React, { Component } from "react";

export class NewsItem extends Component {
  render() {
    return (
      <div>
        <p>{this.props.News.title} </p>
        <div>
          <span>{this.props.News.description}</span> +{" "}
          <span>{this.props.News.IMG}</span>
        </div>
      </div>
    );
  }
}

export default NewsItem;
