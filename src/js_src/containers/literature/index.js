import React, { Component } from 'react';
import { connect } from 'react-redux';

import LitList from './litList';

import { selectActiveEntries } from '../../selectors/litSelectors';

class LiteratureIndexComponent extends Component {
  formatEntries() {
    return this.props.entries;
  }

  renderTabs() {
    return (
      <ul className='tabs'>
        <li className='tabs-title is-active'><a aria-selected='true'>Triage</a></li>
        <li className='tabs-title'><a>Curating</a></li>
      </ul>
    );
  }

  render() {
    let entries = this.formatEntries();
    return (
      <div>
        <h1>Literature in Curation</h1>
        {this.renderTabs()}
        <LitList entries={entries} />
      </div>
    );
  }
}

LiteratureIndexComponent.propTypes = {
  entries: React.PropTypes.array
};


function mapStateToProps(state) {
  return {
    entries: selectActiveEntries(state)
  };
}


export { LiteratureIndexComponent as LiteratureIndexComponent };
export default connect(mapStateToProps)(LiteratureIndexComponent);
