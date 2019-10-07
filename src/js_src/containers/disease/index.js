import React, { Component } from 'react';
import CurateLayout from '../curateHome/layout';
import FileUpload from './fileupload';
import DiseaseForm from './diseaseForm';

class Disease extends Component {
  constructor(props) {
    super(props);
  }

  render() { 
    return (
      <CurateLayout>
        <div className="row">
          <div className="columns small-12 medium-12 large-5">
            <h1>Disease File Upload</h1>
            <FileUpload />
          </div>
          
          <div className="columns small-12 medium-12 large-6 end">
            <h1>Add/Update Disease</h1>
            <DiseaseForm />
          </div>
        </div>
      </CurateLayout>
    );
  }

}

export default Disease;