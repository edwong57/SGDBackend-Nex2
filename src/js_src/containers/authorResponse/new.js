import React, { Component } from 'react';

import AuthorSubmission from '../reserve/authorResponse';

class AuthorResponse extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isComplete: false
    };
  }
  handleSubmitCompletion() {
    this.setState({ isComplete: true });
  }

  render() {
    if (this.state.isComplete) {
      return <h2 style={{ marginTop: '3rem' }}>Thanks for your submission! SGD curators will review your data.</h2>;
    }
    return <AuthorSubmission onComplete={this.handleSubmitCompletion.bind(this)} submitText={'Submit data'} />;
  }
}

export default AuthorResponse;
