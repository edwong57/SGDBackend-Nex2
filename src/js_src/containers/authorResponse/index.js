import React, { Component } from 'react';

import SubmitForm from './submitForm';

class SubmitData extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isComplete: false
    };
  }
  handleSubmitDataCompletion() {
    this.setState({ isComplete: true });
  }

  render() {
    if (this.state.isComplete) {
      return <h2 style={{ marginTop: '3rem' }}>Thanks for your update! SGD curators will review.</h2>;
    }
    return <SubmitForm onComplete={this.handleSubmitDataCompletion.bind(this)} submitText={'Submit update'} />;
  }
}

export default SubmitData;
