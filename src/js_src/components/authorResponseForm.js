import React, { Component } from 'react';
import t from 'tcomb-form';

import FlexiForm from './forms/flexiForm';

class AuthorResponseForm extends Component {
  render() {
    let authorResponseSchema = t.struct({
      pmid: t.maybe(t.String),
      citation: t.maybe(t.String),
      email: t.maybe(t.String),
      display_email: t.maybe(t.Boolean),
      has_function: t.maybe(t.Boolean),
      has_dataset: t.maybe(t.Boolean)
    });
    let formLayout = locals => {
      return (
        <div>
          <p>* indicates required field</p>
          <div className='row'>
            <div className='column small-3'>{locals.inputs.pmid}</div>
            <div className='column small-4'>{locals.inputs.citation}</div>
            <div className='column small-5'>{locals.inputs.email}</div>
          </div>
          <div className='row'>
            <div className='column small-4'>{locals.inputs.has_function}</div>
            <div className='column small-5'>{locals.inputs.has_dataset}</div>
          </div>
        </div>
      );
    };
    let formOptions = {
	template: formLayout,
	fields: {
	    pmid: {
		label: 'Pubmed ID for your paper * : '
	    },
	    citation: {
		label: 'Citation for your paper: '
	    },
	    email: {
		label: 'Your E-mail address * : '
	    }
	}
    };
    let _onSuccess = (data) => {
      if (this.props.onComplete) this.props.onComplete(data.colleague_id);
    };
    let _requestMethod = this.props.requestMethod || 'PUT';
    let _submitText = this.props.submitText || 'Approve Changes';
    return <FlexiForm defaultData={this.props.defaultData} tFormOptions={formOptions} tFormSchema={authorResponseSchema} onSuccess={_onSuccess} requestMethod={_requestMethod} submitText={_submitText} updateUrl={this.props.submitUrl} />;
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
