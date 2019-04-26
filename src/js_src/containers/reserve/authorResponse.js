import React, { Component } from 'react';
import { connect } from 'react-redux';
// import { push } from 'react-router-redux';
// import { Async } from 'react-select';

import AuthorResponseForm from '../../components/authorResponseForm';
import fetchData from '../../lib/fetchData';
import Loader from '../../components/loader';

// const AUTOCOMPLETE_BASE = '/autocomplete_results?category=colleague&q=';
const AUTHOR_RESPONSE_BASE = '/authorResponse';

class AuthorResponse extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      pmid: null,
      citation: null,
      selectorValue: null,
      formValue: null,
      isPending: false
    };
  }

  handleSelect(value) {
    if (Array.isArray(value)) {
	this.setState({ selectorValue: null, pmid: null, citation: null });
    }
    this.setState({ selectorValue: value });
    // fetch data to update form
    let url = `${AUTHOR_RESPONSE_BASE}/${value.formatName}`;
    this.setState({ isPending: true });
    fetchData(url).then( data => {
      this.setState({ formValue: data, isPending: false, pmid: data.pmid });
    });
  }

  renderSelector() {
    let getOptions = (input, callback) => {
      if (input === '') {
        callback(null, {
          options: [],
          complete: false
        });
      }

      // let url = `${AUTOCOMPLETE_BASE}${input}`;
      // fetchData(url).then( data => {
      //  let results = data.results || [];
      //  let _options = results.map( d => {
      //    let institution =  d.institution ? `, ${d.institution}` : '';
      //    return {
      //      label: `${d.name}${institution}`,
      //      formatName: d.format_name
      //    };
      //  });
      //  callback(null, {
      //    options: _options,
      //    complete: false
      //  });
      // });
    };

    // WORK FROM HERE

    return (
      <div style={{ marginBottom: '1rem' }}>
        <p>Information about your recently published paper</p>
      <p>Please tell us about your paper and help us keep SGD up to date:</p>
        <div className='row'>
          <div className='columns small-12 medium-6'>
            {selectNode}
          </div>
          <div className='columns small-12 medium-6'>
               SECTION HERE
          </div>
        </div>
      </div>
    );
  }

  renderForm() {
    if (this.state.isPending) return <Loader />;
    if (!this.state.selectorValue) return null;
    let _requestMethod = 'POST';
    let url = 'authorResponse';
    let _submitText = this.props.submitText || 'Next';
    return <AuthorResponseForm defaultData={this.state.formValue} onComplete={this.props.onComplete.bind(this)} requestMethod={_requestMethod} submitUrl={url} submitText={_submitText} />;
  }

  render() {
    return (
      <div>
        {this.renderSelector()}
        {this.renderForm()}
      </div>
    );
  }
}

AuthorResponse.propTypes = {
  dispatch: React.PropTypes.func,
  onComplete: React.PropTypes.func,
  submitText: React.PropTypes.string
};

function mapStateToProps() {
  return {
  };
}

export default connect(mapStateToProps)(AuthorResponse);
