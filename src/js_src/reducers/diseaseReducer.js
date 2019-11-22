const DEFAULT_STATE = {
  currentDisease: {
    annotation_id: 0,
    dbentity_id: '',
    taxonomy_id: '',
    reference_id: '',
    eco_id: '',
    association_type: '',
    disease_id: '',
    with_ortholog: '',
    annotation_type: '',
  }
};

const SET_DISEASE = 'SET_DISEASE';

const diseaseReducer = (state = DEFAULT_STATE, action) => {
  switch (action.type) {
  case SET_DISEASE:
    return Object.assign({}, state, action.payload);
  default:
    return state;
  }
};

export default diseaseReducer;