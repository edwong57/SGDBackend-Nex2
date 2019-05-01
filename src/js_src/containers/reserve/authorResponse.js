import React, { Component } from 'react';
import { connect } from 'react-redux';

import AuthorResponseForm from '../../components/authorResponseForm';
import Loader from '../../components/loader';

class AuthorResponse extends Component {

  // selectorValue: null, 
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      pmid: null,
      citation: null,
      email: null,
      has_novel_data: false,
      has_large_scale_data: false,
      novel_research_result: null,
      dataset_desc: null,
      gene_list: null,
      other_desc: null,
      formValue: null,
      isPending: false
    };
  }

  handleHasNovelDataChange() {
    this.setState({ has_novel_data: !this.state.has_novel_data });
  }

  handleHasLargeScaleDataChange() {
    this.setState({ has_large_scale_data: !this.state.has_large_scale_data });
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
               <p>Your E-mail address <font color='red'>(Required)</font>: <textarea ref='email' value={this.state.email} name='email' rows='1' cols='50'></textarea></p>
               <p>Does this paper contain novel characterizations of the function, role, or localization of a gene product(s)? <input checked={this.state.has_novel_data} onChange={this.handleHasNovelDataChange.bind(this)} type='checkbox' /> Yes<br></br>
               If yes, please summarize briefly the novel results. <textarea ref='novel_research_result' value={this.state.novel_research_result} name='novel_research_result' rows='3' cols='50'></textarea></p>
               <p>If this paper focuses on specific genes/proteins, please identify them here (enter a list of gene names/systematic names): <textarea ref='gene_list' value={this.state.gene_list} name='gene_list' rows='1' cols='50'></textarea></p>
               <p>Does this study include large-scale datasets that you would like to see incorporated into SGD? <input checked={this.state.has_large_scale_data} onChange={this.handleHasLargeScaleDataChange.bind(this)} type='checkbox' /> Yes<br></br>
               If yes, please describe briefly the type(s) of data. <textarea ref='dataset_desc' value={this.state.dataset_desc} name='dataset_desc' rows='3' cols='50'></textarea></p> 
               <p>Is there anything else that you would like us to know about this paper? <textarea ref='other_desc' value={this.state.other_desc} name='other_desc' rows='3' cols='50'></textarea></p>
               <p><input type="submit" value="Submit" className="button secondary"></input></p>
          </div>
        </div>
      </div>
    );
  }

  renderForm() {
    if (this.state.isPending) return <Loader />;
    // if (!this.state.selectorValue) return null;
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
