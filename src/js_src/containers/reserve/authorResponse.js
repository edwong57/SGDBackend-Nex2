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
        <center><h3>Information about your recently published paper</h3></center>
           <p>Please tell us about your paper and help us keep SGD up to date:</p>
        <div className='row'>
          <div className='large-12 columns'>
               <p>Pubmed ID for your paper <font color='red'>(Required)</font>: <textarea ref='pmid' value={this.state.pmid} name='pmid' rows='1' cols='50'></textarea></p>
               <p>Citation for your paper: <textarea ref='citation' value={this.state.citation} name='citation' rows='1' cols='50'></textarea></p>
               <p>Your E-mail address <font color='red'>(Required)</font>: <textarea ref='email' value={this.state.email} name='pmid' rows='1' cols='50'></textarea></p>
               <p>Does this paper contain novel characterizations of the function, role, or localization of a gene product(s)? 
               <input checked={this.state.hasFunction} onChange={this.handleHasFunctionChange.bind(this)} type='checkbox' /> Yes<br></br>
               If yes, please summarize briefly the novel results. <textarea ref='function' value={this.state.function} name='function' rows='5' cols='50'></textarea></p>
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
