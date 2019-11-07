import React, { Component } from "react";
import Axios from "axios";
import Parser from "html-react-parser";
import "./styles/News.css";

export default class News extends Component {
  state = {
    title: [],
    summary: [],
    thumbnail: [],
    publish_date: [],
    content: [],
    url: []
  };
  componentDidMount() {
    const id = this.props.match.params.id;
    Axios.get("http://localhost:5000/news/" + id)
      .then(res => {
        console.log(res.data);

        const {
          title,
          summary,
          thumbnail,
          publish_date,
          content,
          url
        } = res.data;
        this.setState({
          title,
          summary,
          thumbnail,
          publish_date,
          content,
          url
        });
        console.log(this.state);
      })
      .catch(err => console.log(err));
  }
  render() {
    return this.state.content.length === 0 ? (
      <div> </div>
    ) : (
      <div dir="rtl">
        <div className="page-header">
          <div className="title">
            <div className="title-text">{this.state.title} </div>
          </div>
          <img
            className="page-image"
            src={this.state.thumbnail}
            alt="No Image :("
          />
        </div>
        <div className="page-body">
          <h4 className="summary">{this.state.summary}</h4>
          <br />
          <br />
          {Parser(this.state.content)}
          <br />
        </div>
        <div className="footer">
          <span>تاریخ انتشار : {this.state.publish_date}</span>
          <a className="site-link" href={"https://www." + this.state.url}>
            لینک به خبر اصلی
          </a>
        </div>
      </div>
    );
  }
}
