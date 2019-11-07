import React, { Component } from "react";
import "./styles/NewsItem.css";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export class NewsItem extends Component {
  render() {
    console.log(this.props);
    const { id, title, summary, thumbnail, publish_date } = this.props.News;
    return (
      <div className="item">
        <Link to={`/results/${id}`}>
          <p>{title} </p>
        </Link>

        <div>
          <span className="summary">{summary}</span>
          <span>
            <img className="image" src={thumbnail} alt="img here" />
          </span>
        </div>
      </div>
    );
  }
}

NewsItem.propTypes = {
  News: PropTypes.object.isRequired
};

export default NewsItem;
