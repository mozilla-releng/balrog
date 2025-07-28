import { stringify } from 'qs';
import {
  getRequiredSignoffs,
  getScheduledChanges,
} from '../../../services/requiredSignoffs';
import { OBJECT_NAMES } from '../../../utils/constants';
import RequiredSignoffs from '../ListSignoffs/RequiredSignoffs';

// A utlity to holds all of the Required Signoffs - product, permissions,
// and scheduled changes
export default async (product, channel) => {
  const requiredSignoffs = new RequiredSignoffs();
  const withQuery = (url) => {
    if (url.includes(OBJECT_NAMES.PERMISSIONS_REQUIRED_SIGNOFF)) {
      return url + stringify({ product }, { addQueryPrefix: true });
    }

    return url + stringify({ product, channel }, { addQueryPrefix: true });
  };

  const [
    {
      data: { required_signoffs: productRS },
    },
    {
      data: { required_signoffs: permissionsRS },
    },
    {
      data: { scheduled_changes: productSC },
    },
    {
      data: { scheduled_changes: permissionsSC },
    },
  ] = await Promise.all([
    getRequiredSignoffs(withQuery(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF)),
    getRequiredSignoffs(withQuery(OBJECT_NAMES.PERMISSIONS_REQUIRED_SIGNOFF)),
    getScheduledChanges(withQuery(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF)),
    getScheduledChanges(withQuery(OBJECT_NAMES.PERMISSIONS_REQUIRED_SIGNOFF)),
  ]);

  requiredSignoffs.setProductRequiredSignoffs(productRS);
  requiredSignoffs.setPermissionsRequiredSignoffs(permissionsRS);
  requiredSignoffs.setProductScheduledChanges(productSC);
  requiredSignoffs.setPermissionScheduledChanges(permissionsSC);

  return requiredSignoffs.value();
};
