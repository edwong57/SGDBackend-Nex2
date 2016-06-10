import React from 'react';
import { connect } from 'react-redux';

const ColleaguesShow = React.createClass({
  getInitialState () {
    return {
      data: null,
      isPending: false
    };
  },

  render () {
    if (this.state.isPending) return <Loader />;
    if (!this.state.data) return null;
    let data = this.state.data;
    return (
      <div>
        <h1>{data.first_name} {data.last_name}</h1>
        <hr />
        {this._renderInfoField('email', 'envelope')}
        {this._renderInfoField('position', 'flask')}
        {this._renderInfoField('profession', 'clipboard')}
        {this._renderInfoField('organization', 'university')}
        {this._renderInfoField('orcid', 'info')}
        {this._renderInfoField('work_phone', 'phone')}
        {this._renderAddress()}
        {this._renderResearchInterests()}
        {this._renderKeywords()}
        {this._renderWebpages()}
      </div>
    );
  },

  componentDidMount () {
    this._fetchData();
  },

  _renderInfoField (fieldName, iconClass) {
    let data = this.state.data;
    if (!data[fieldName]) return null;
    let iconNode = (iconClass) ? <span><i className={`fa fa-${iconClass}`} /> </span> : null;
    return <p>{iconNode}{data[fieldName]}</p>;
  },

  _renderAddress () {
    let data = this.state.data;
    let addressArray = data.address || [];
    let city = (data.city) ? `${data.city}, ` : '';
    let state = (data.state) ? `${data.state} `: '';
    let postal_code = (data.postal_code) ? `${data.postal_code} `: '';
    let country = (data.country) ? `${data.country} `: '';
    addressArray.push(`${city}${state}${postal_code}${country}`);
    let nodes = addressArray.map( (d, i) => {
      return <p key={`colAdd${i}`}>{d}</p>;
    });
    return (
      <div>
        <label>Address</label>
        {nodes}
      </div>
    );
  },

  _renderResearchInterests () {
    let interests = this.state.data.research_interests;
    if (!interests) return null;
    let nodes = interests.split(', ').map( (d, i) => {
      return <p key={`colRI${i}`}>{d}</p>;
    });
    return (
      <div>
        <label>Research Interests</label>
        {nodes}
      </div>
    );
  },

  _renderKeywords () {
    let keywords = this.state.data.keywords;
    if (!keywords) return null;
    let nodes = keywords.map( (d, i) => {
      return <p key={`colKW${i}`}>{d}</p>;
    });
    return (
      <div>
        <label>Keywords</label>
        {nodes}
      </div>
    );
  },

  _renderWebpages () {
    let webpages = this.state.data.webpages;
    if (!webpages) return null;
    return (
      <div>
        <label>Webpages</label>
        <p>Lab URL: <a href={webpages.lab_url}>{webpages.lab_url}</a></p>
        <p>Research Summary: <a href={webpages.research_summary_url}>{webpages.research_summary_url}</a></p>
      </div>
    );
  },

  _fetchData () {
    this.setState({ isPending: true });
    let displayName = this.props.routeParams.colleagueDisplayName;
    fetch(`${COLLEAGUE_GET_URL}/${displayName}`, {
      credentials: 'same-origin',
    }).then( response => {
      return response.json();
    }).then( json => {
      this.setState({ data: json, isPending: false });
    });
  }
});

function mapStateToProps(_state) {
  return {
  };
}

export default connect(mapStateToProps)(ColleaguesShow);
