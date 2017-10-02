import React, { Component } from 'react';
import { connect } from 'react-redux';

import TagList from '../../components/tagList';
import Loader from '../../components/loader';
import fetchData from '../../lib/fetchData';
import { clearTags, updateTags } from './litActions';
import { setError, clearError, setPending, finishPending} from '../../actions/metaActions';

class Tags extends Component {
  componentDidMount() {
    this.fetchData();
  }

  handleSave(e) {
    e.preventDefault();
    let id = this.props.id;
    let url = `/reference/${id}/tags`;
    let options = {
      data: JSON.stringify({ tags: this.props.activeTags }),
      type: 'PUT'
    };
    this.props.dispatch(setPending());
    fetchData(url, options).then( data => {
      this.props.dispatch(updateTags(data));
      this.props.dispatch(clearError());
      this.props.dispatch(finishPending());
    }).catch( (data) => {
      let errorMessage = data ? data.error : 'There was an updating tags.';
      this.props.dispatch(setError(errorMessage));
      this.props.dispatch(finishPending());
    });
  }

  fetchData() {
    let id = this.props.id;
    let url = `/reference/${id}/tags`;
    this.props.dispatch(clearTags());
    fetchData(url).then( data => {
      this.props.dispatch(updateTags(data));
    });
  }

  render() {
    if (this.props.isPending) return <Loader />;
    let _onUpdate = newEntry => {
      this.props.dispatch(updateTags(newEntry));
    };
    return (
      <div>
        <TagList tags={this.props.activeTags} onUpdate={_onUpdate} />
        <a className='button' onClick={this.handleSave.bind(this)} style={{ marginTop: '1rem' }}>Save</a>
      </div>
    );
  }
}

Tags.propTypes = {
  activeTags: React.PropTypes.array,
  dispatch: React.PropTypes.func,
  id: React.PropTypes.string,
  isPending: React.PropTypes.bool
};

function mapStateToProps(state) {
  return {
    activeTags: state.lit.get('activeTags').toJS(),
    isPending: state.meta.get('isPending')
  };
}

export default connect(mapStateToProps)(Tags);
