import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import style from './style.css';
import SingleFilterSelector from './singleFilterSelector';
import { getQueryParamWithValueChanged } from '../../../lib/searchHelpers';
import CategoryLabel from '../../../components/categoryLabel';
import {parse} from 'query-string';

import {
  selectActiveCategory,
  selectAggregations,
  selectIsPending
} from '../../../selectors/searchSelectors';

class FilterSelectorComponent extends Component {
  renderFilters() {
    let aggs = this.props.aggregations;
    if (aggs.length === 0) {
      return <p>No filters available.</p>;
    }
    // if on cat selector and pending, render nothing
    if (this.props.activeCategory === 'none' && this.props.isPending) {
      return null;
    }
    return aggs.map( d => {
      return <div key={`filter${d.name}`}><SingleFilterSelector {...d} queryParams={this.props.queryParams} /></div>;
    });
  }

  renderCatSelector() {
    let cat = this.props.activeCategory;
    if (cat === 'none') {
      return null;
    }
    let newQp = getQueryParamWithValueChanged('category', [], this.props.queryParams, true);
    let newHref = { pathname: '/search', query: newQp };
    return (
      <div>
        <p><CategoryLabel category={this.props.activeCategory} /></p>
        <p>
          <Link to={newHref}><i className='fa fa-chevron-left' /> Show all Categories</Link>
        </p>
      </div>
    );
  }

  render() {
    return (
      <div className={style.aggContainer} >
        {this.renderCatSelector()}
        {this.renderFilters()}
      </div>
    );
  }
}

FilterSelectorComponent.propTypes = {
  activeCategory: PropTypes.string,
  aggregations: PropTypes.array,
  isPending: PropTypes.bool,
  queryParams: PropTypes.object
};

function mapStateToProps(state) {
  let location = state.router.location;
  let _queryParams = location ? parse(location.search) : {};
  return {
    activeCategory:  selectActiveCategory(state),
    aggregations: selectAggregations(state),
    isPending: selectIsPending(state),
    queryParams: _queryParams
  };
}

export { FilterSelectorComponent as FilterSelectorComponent };
export default connect(mapStateToProps)(FilterSelectorComponent);
