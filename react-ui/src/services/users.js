import axios from 'axios';

const getUsers = () => axios.get('/users');
const getUserInfo = username => axios.get(`/users/${username}`);

export { getUsers, getUserInfo };
