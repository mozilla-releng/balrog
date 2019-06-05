import axios from 'axios';
import { stringify } from 'qs';

const baseUrl = `${process.env.BALROG_ROOT_URL}/api`;
const getHistory = params => {
  const url = `${baseUrl}/${params.object}/history`;
  const qs = stringify(
    {
      changed_by: params.changedBy,
      timestamp_from: params.dateTimeStart,
      timestamp_to: params.dateTimeEnd,
      product: params.product,
      channel: params.channel,
    },
    { addQueryPrefix: true }
  );

  return axios.get(`${url}${qs}`);
};

// History factory
// eslint-disable-next-line import/prefer-default-export
export { getHistory };
