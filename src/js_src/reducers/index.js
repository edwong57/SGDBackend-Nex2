import authReducer from './authReducer';
import metaReducer from './metaReducer';
import litReducer from './litReducer';
import locusReducer from './locusReducer';
import searchReducer from './searchReducer';
import ptmReducer from './ptmReducer';
import newsLetterReducer from './newsLetterReducer';
import regulationReducer from './regulationReducer';
import phenotypeReducer from './phenotypeReducer';
import authorResponseReducer from './authorResponseReducer';

export default {
  auth: authReducer,
  meta: metaReducer,
  lit: litReducer,
  locus: locusReducer,
  search: searchReducer,
  ptm:ptmReducer,
  newsLetter:newsLetterReducer,
  regulation:regulationReducer,
  phenotype:phenotypeReducer,
  authorResponse:authorResponseReducer
};
