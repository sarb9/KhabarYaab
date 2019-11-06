import React, { Component } from "react";
import "./styles/NewsItem.css";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export class NewsItem extends Component {
  render() {
    console.log(this.props);
    const { title, description, IMG } = this.props.News;
    const id = this.props.id;
    return (
      <div className="item">
        <Link to={`/result/${id}`}>
          <p>{title} </p>
        </Link>

        <div>
          <span className="description">{description}</span>
          <span>
            <img className="image" src={IMG} alt="img here" />
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
