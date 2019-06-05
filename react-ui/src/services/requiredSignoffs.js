import axios from 'axios';
import { BASE_URL } from '../utils/constants';

const getRequiredSignoffs = objectName =>
  axios.get(`${BASE_URL}/${objectName}`);
const getScheduledChanges = objectName =>
  axios.get(`${BASE_URL}/scheduled_changes/${objectName}`);

// requiredSignoffs factory
export default {
  getRequiredSignoffs,
  getScheduledChanges,
};
