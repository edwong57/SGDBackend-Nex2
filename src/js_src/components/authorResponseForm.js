import React, { Component } from 'react';
import t from 'tcomb-form';

import FlexiForm from './forms/flexiForm';

class AuthorResponseForm extends Component {
  render() {
    let colleagueSchema = t.struct({
      pmid: t.maybe(t.String),
      citation: t.maybe(t.String),
      email: t.maybe(t.String),
      has_function: t.maybe(t.Boolean),
      has_dataset: t.maybe(t.Boolean)
    });
    let formLayout = locals => {
      return (
        <div>
          <p>* indicates required field</p>
          <div className='row'>
            <div className='column small-3'>{locals.inputs.first_name}</div>
            <div className='column small-4'>{locals.inputs.last_name}</div>
            <div className='column small-5'>{locals.inputs.email}</div>
          </div>
          <div className='row'>
            <div className='column small-3'>{locals.inputs.display_email}</div>
            <div className='column small-4'>{locals.inputs.receive_quarterly_newsletter}</div>
            <div className='column small-5'>{locals.inputs.willing_to_be_beta_tester}</div>
          </div>
          <span><a href='https://orcid.org/register' target='_new'><i className='fa fa-question-circle' /> Register for an ORCID iD</a></span>
          <div className='row'>
            <div className='column small-3'>{locals.inputs.orcid}</div>
          </div>
        </div>
      );
    };
    let colleagueOptions = {
      template: formLayout,
      fields: {
        pmid: {
          label: 'Pubmed ID for your paper: *'
        },
        last_name: {
          label: 'Last Name *'
        },
        email: {
          label: 'Email *'
        },
        orcid: {
          label: 'ORCID iD *'
        }
      }
    };
    let _onSuccess = (data) => {
      if (this.props.onComplete) this.props.onComplete(data.colleague_id);
    };
    let _requestMethod = this.props.requestMethod || 'PUT';
    let _submitText = this.props.submitText || 'Approve Changes';
    return <FlexiForm defaultData={this.props.defaultData} tFormOptions={colleagueOptions} tFormSchema={colleagueSchema} onSuccess={_onSuccess} requestMethod={_requestMethod} submitText={_submitText} updateUrl={this.props.submitUrl} />;
  }
}

AuthorResponseForm.propTypes = {
  defaultData: React.PropTypes.object,
  onComplete: React.PropTypes.func,
  requestMethod: React.PropTypes.string,
  submitText: React.PropTypes.string,
  submitUrl: React.PropTypes.string
};

export default AuthorResponseForm;
