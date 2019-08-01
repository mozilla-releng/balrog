import axios from 'axios';

const getHistory = (object, qs) => axios.get(`/${object}/history/${qs}`);

// History factory
// eslint-disable-next-line import/prefer-default-export
export { getHistory };
