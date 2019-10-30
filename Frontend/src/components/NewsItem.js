import React, { Component } from "react";
import "./styles/NewsItem.css";
import PropTypes from "prop-types";

export class NewsItem extends Component {
  render() {
    const { title, description, IMG } = this.props.News;
    return (
      <div className="item">
        <p>{title} </p>
        <div>
          <span>{description}</span> + <span>{IMG}</span>
        </div>
      </div>
    );
  }
}

NewsItem.propTypes = {
  News: PropTypes.object.isRequired
};

export default NewsItem;
