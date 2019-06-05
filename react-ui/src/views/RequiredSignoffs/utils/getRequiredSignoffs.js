import { stringify } from 'qs';
import { OBJECT_NAMES } from '../../../utils/constants';
import RequiredSignoffs from '../ListSignoffs/RequiredSignoffs';
import rsService from '../../../services/requiredSignoffs';

// A utlity to holds all of the Required Signoffs - product, permissions,
// and scheduled changes
export default async (product, channel) => {
  const requiredSignoffs = new RequiredSignoffs();
  const withQuery = url => {
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
    rsService.getRequiredSignoffs(
      withQuery(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF)
    ),
    rsService.getRequiredSignoffs(
      withQuery(OBJECT_NAMES.PERMISSIONS_REQUIRED_SIGNOFF)
    ),
    rsService.getScheduledChanges(
      withQuery(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF)
    ),
    rsService.getScheduledChanges(
      withQuery(OBJECT_NAMES.PERMISSIONS_REQUIRED_SIGNOFF)
    ),
  ]);

  requiredSignoffs.setProductRequiredSignoffs(productRS);
  requiredSignoffs.setPermissionsRequiredSignoffs(permissionsRS);
  requiredSignoffs.setProductScheduledChanges(productSC);
  requiredSignoffs.setPermissionScheduledChanges(permissionsSC);

  return requiredSignoffs.value();
};
