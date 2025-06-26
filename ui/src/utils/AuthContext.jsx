import React, { useContext, createContext } from 'react';

export const AuthContext = createContext({
  authorize: Function.prototype,
  unauthorize: Function.prototype,
  user: null,
});

export function withUser(UnauthedComponent) {
  return function AuthorizableComponent(props) {
    const { authorize, unauthorize, user } = useContext(AuthContext);

    return (
      <UnauthedComponent
        {...props}
        onAuthorize={authorize}
        onUnauthorize={unauthorize}
        user={user && user.userInfo}
      />
    );
  };
}
