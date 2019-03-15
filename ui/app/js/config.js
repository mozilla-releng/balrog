// This file is not packaged with the app; it must be provided as part of the deployment environment
angular.module("config", [])
.constant("Auth0Config", {
    domain: "auth.mozilla.auth0.com",
    audience: "login.taskcluster.net",
    clientID: "FK1mJkHhwjulTYBGklxn8W4Fhd1pgT4t",
    redirectUri: "https://localhost:8010/login"
});
