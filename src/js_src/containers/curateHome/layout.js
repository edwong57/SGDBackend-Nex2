import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import style from './style.css';
import { SMALL_COL_CLASS, LARGE_COL_CLASS,ml_12 } from '../../constants';
import Badge from '@material-ui/core/Badge';

class CurateLayout extends Component {
  render() {
    let location = this.props.location ? this.props.location.pathname : '';
    let colleagueCount = this.props.colleagueCount ? this.props.colleagueCount : 0;
    let geneCount = this.props.geneCount ? this.props.geneCount : 0; 
    // console.log(this.props.location);
    return (
      <div className='row'>
        <div className={SMALL_COL_CLASS}>
          <ul className='vertical menu'>
            {/* spans added of Link to address https://stackoverflow.com/questions/38796376/cannot-read-property-gethostnode-of-null */}
            <li><Link className={(location === '/') ? style.activeLink : null} to=''><span><i className='fa fa-home' /> Home</span></Link></li>
            <li><Link className={(location === '/triage') ? style.activeLink : null} to='/triage'><span><i className='fa fa-book' /> Lit Triage</span></Link></li>
            <li><Link className={(location === '/colleagues/triage') ? style.activeLink : null} to='/colleagues/triage'><span><i className='fa fa-users' /> Colleague Updates <span style={ml_12}><Badge badgeContent={colleagueCount} color="error" /></span></span></Link></li>
            <li><Link className={(location.match('/reservations')) ? style.activeLink : null} to='/reservations'><span><i className='fa fa-sticky-note' /> Gene Name Reservations <span style={ml_12}><Badge badgeContent={geneCount} color="error" /></span></span></Link></li>
            <li><Link className={(location === '/spreadsheet_upload') ? style.activeLink : null} to='/spreadsheet_upload'><span><i className='fa fa-upload' /> Spreadsheet Upload</span></Link></li>
            <li><Link className={(location === '/settings') ? style.activeLink : null} to='/settings'><span><i className='fa fa-cog' /> Settings</span></Link></li>
            <li><Link className={(location === '/curate/reference/new') ? style.activeLink : null} to='/curate/reference/new'><span><i className='fa fa-plus' /> Add References</span></Link></li>
            <li><Link className={(location === '/newsletter') ? style.activeLink : null} to='/newsletter'><span><i className="fa fa-envelope" /> Newsletter</span></Link></li>
            <li><Link className={(location === '/ptm') ? style.activeLink : null} to='/ptm'><span><i className="fa fa-upload" /> PTM</span></Link></li>
            <li><Link className={(location === '/regulation') ? style.activeLink : null} to='/regulation'><span><i className="fa fa-upload" /> Regulation</span></Link></li>
            <li><Link className={(location === '/disease') ? style.activeLink : null} to='/disease'><span><i className="fa fa-upload" /> Disease</span></Link></li>
            <li><Link className={(location === '/file_curate') ? style.activeLink : null} to='/file_curate'><span><i className='fa fa-file-text' /> File Curate</span></Link></li>
            <li><span><Link className={(location === '/new_phenotype') ? style.activeLink : null} to='/new_phenotype'><i className='fa fa-sticky-note' />Phenotype NEW</Link> | <Link className={(location === '/search_phenotype') ? style.activeLink : null} to='/search_phenotype'>UPDATE</Link></span></li>
            <li><span><Link className={(location === '/litguide_todo') ? style.activeLink : null} to='/litguide_todo'><i className='fa fa-sticky-note' />LitGuide TODO</Link> | <Link className={(location === '/add_litguide') ? style.activeLink : null} to='/add_litguide'>ADD</Link></span></li>
            <li><Link className={(location.match('/author_responses')) ? style.activeLink : null} to='/author_responses'><span><i className='fa fa-sticky-note' /> Author Response </span></Link></li>
          </ul>
        </div>
        <div className={LARGE_COL_CLASS}>
          <div>
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}

CurateLayout.propTypes = {
  children: PropTypes.object,
  location: PropTypes.object,
  geneCount:PropTypes.number,
  colleagueCount:PropTypes.number
};

function mapStateToProps(state) {
  return {
    location: state.router.location,
    geneCount:state.meta.get('geneCount'),
    colleagueCount:state.meta.get('colleagueCount')
  };
}

export { CurateLayout as CurateLayout };
export default connect(mapStateToProps)(CurateLayout);
