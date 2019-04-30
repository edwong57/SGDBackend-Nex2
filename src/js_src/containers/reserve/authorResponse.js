import React, { Component } from 'react';
import { connect } from 'react-redux';

import AuthorResponseForm from '../../components/authorResponseForm';
import Loader from '../../components/loader';

class AuthorResponse extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      pmid: null,
      citation: null,
      hasFunction: false,
      selectorValue: null,
      formValue: null,
      isPending: false
    };
  }

  handleHasFunctionChange() {
    this.setState({ hasFunction: !this.state.hasFunction });
  }

  renderSelector() {

    return (
      <div style={{ marginBottom: '1rem' }}>
        <center><p>Information about your recently published paper</p></center>
           <br></br>
           <p>Please tell us about your paper and help us keep SGD up to date:</p>
        <div className='row'>
          <div className='large-12 columns'>
               <p>Pubmed ID for your paper: <textarea ref='pmid' value={this.state.pmid}  name='pmid' rows='1' cols='50'></textarea> <font color='red'>(Required)</font></p>
      <p>Pubmed ID for your paper <font color='red'>(Required)</font>: <textfield ref='pmid' value={this.state.pmid}  name='pmid' size='50'></textfield> <font color='red'>(Required)</font></p>
               Does this paper contain novel characterizations of the function, role, or localization of a gene product(s)? 
               <input checked={this.state.hasFunction} onChange={this.handleHasFunctionChange.bind(this)} type='checkbox' /> Yes

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
