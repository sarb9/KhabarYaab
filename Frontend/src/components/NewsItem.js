import React, { Component } from "react";
import "./styles/NewsItem.css";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import Parser from "html-react-parser";

export class NewsItem extends Component {
  render() {
    const {
      id,
      title,
      selected_parts,
      thumbnail,
      publish_date,
      news_date,
      url
    } = this.props.News;
    return (
      <div className="item" dir="rtl">
        <Link to={`/results/${id}`}>
          <p>{title} </p>
        </Link>

        <div>
          <span className="selected-parts">{Parser(selected_parts)}</span>
          <span>
            <img className="image" src={thumbnail} alt="No Img :(" />
          </span>
          <br />
          <br />
        </div>
        <div>
          <span>تاریخ انتشار : {publish_date}</span>
          <a className="site-link" href={"https://www." + url}>
            لینک به خبر اصلی
          </a>
        </div>
      </div>
    );
  }
}

NewsItem.propTypes = {
  News: PropTypes.object.isRequired
};

export default NewsItem;
