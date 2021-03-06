/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
class EditableList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      values: props.defaultValues || []
    };
  }

  // call onUpdate prop if defined and values changed
  componentDidUpdate(prevProps, prevState) {
    if (this.state.values !== prevState.values && typeof this.props.onUpdate === 'function') {
      this.props.onUpdate(this.state.values);
    }
  }

  renderValues () {
    let nodes = this.state.values.map( (d, i) => {
      return <li key={`editLI${i}`}>{d}</li>;
    });
    return (
      <ul>{nodes}</ul>
    );
  }

  handleAddValue (e) {
    e.preventDefault();
    let content = this.refs.inputText.value;
    if (content === '') return; // ignore blank
    let newValues = this.state.values.slice();
    newValues.push(content);
    this.setState({ values: newValues });
    // clear input
    this.refs.inputText.value = '';
  }

  render () {
    return (
      <div>
        {this.renderValues()}
        <input placeholder={this.props.placeholder} ref='inputText' type='text' />
        <div className='text-right'>
          <a className='button secondary small' onClick={this.handleAddValue.bind(this)}>Add</a>
        </div>
      </div>
    );
  }
}

EditableList.propTypes = {
  defaultValues: PropTypes.array,
  onUpdate: PropTypes.func, // onUpdate(values)
  placeholder: PropTypes.string
};

export default EditableList;
