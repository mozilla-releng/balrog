import { stringify } from 'qs';
import axios from 'axios';

const getHistory = params => {
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

  return axios.get(`/${params.object}/history/${qs}`);
};

// History factory
// eslint-disable-next-line import/prefer-default-export
export { getHistory };
