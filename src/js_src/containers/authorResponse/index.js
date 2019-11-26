import React, { Component } from 'react';

import AuthorResponse from './authorResponse';

class SubmitData extends Component {
    constructor(props) {
	super(props);
	this.state = {
	    isComplete: false
	};
    }
    handleColleagueCompletion() {
	this.setState({ isComplete: true });
    }

    render() {
	if (this.state.isComplete) {
	    return <h2 style={{ marginTop: '3rem' }}>Thanks for your update! SGD curators will review.</h2>;
	}
	return <AuthorResponse onComplete={this.handleColleagueCompletion.bind(this)} />;
    }
}

export default SubmitData;
