
describe("controller: UserPermissionsCtrl", function() {

  beforeEach(function() {
    module("app");
  });

  var user = {
    username: "peterbe"
  };
  var users = [
    {
      username: "peterbe",
      roles: [
        { 'role': 'qa', 'data_version': 1 },
        { 'role': 'releng', 'data_version': 1 }
      ]
    }, {
      username: "bhearsum",
      roles: [
        { 'role': 'qa', 'data_version': 1 },
        { 'role': 'releng', 'data_version': 1 }
      ]
    }];

  var sample_permissions = {
    "permissions": {
      "/releases/:name": {
        data_version: 1,
        options: null
      }
    },
    "roles": {}
  };

  var sample_roles = {
    'roles': [
      { 'role': 'qa', 'data_version': 1 },
      { 'role': 'releng', 'data_version': 1 }
    ]
  };
  var sample_all_roles = {
    'roles': [
      { 'role': 'qa', 'data_version': 1 },
      { 'role': 'releng', 'data_version': 1 }
    ]
  };
  var signoffRequirements = [];

  beforeEach(inject(function($controller, $rootScope, $location, $modal, Permissions, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');

    $controller('UserPermissionsCtrl', {
      $scope: this.scope,
      $modalInstance: $modal.open({
        templateUrl: 'rule_modal.html'
      }),
      $location: $location,
      Permissions: Permissions,
      user: user,
      is_edit: true,
      users: users,
      roles:sample_all_roles.roles,
      permissionSignoffRequirements: signoffRequirements,
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the edit user modal", function() {

    it("should should all defaults", function() {
      this.$httpBackend.expectGET('/api/users/peterbe')
      .respond(200, JSON.stringify(sample_permissions));
      this.$httpBackend.flush();
      expect(this.scope.errors).toEqual({permissions:{}});
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.loading).toEqual(false);
      expect(this.scope.user).toEqual({
        username: "peterbe",
        permissions: [
          {
            permission: "/releases/:name",
            options: null,
            data_version: 1
          }
          // {
          //   permission: "admin",
          //   options: null,
          //   data_version: 1
          // }
        ],
        roles: [
          { 'role': 'qa', 'data_version': 1 },
          { 'role': 'releng', 'data_version': 1 }
        ]
      });
      // expect(this.scope.user.username).toEqual('peterbe');
      expect(this.scope.is_edit).toEqual(true);
    });
    //
    it("should should be able add a permission", function() {
      this.$httpBackend.expectGET('/api/users/peterbe')
      .respond(200, JSON.stringify(sample_permissions));
      this.$httpBackend.flush();
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      this.$httpBackend.expectPUT('/api/users/peterbe/permissions/admin')
      .respond(201, JSON.stringify({new_data_version: 1}));

      this.scope.permission.permission = 'admin';
      this.scope.addPermission();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.user.permissions.length).toEqual(2);
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.errors).toEqual({permissions:{}});
    });

    it("should should be able update a permission", function() {
      this.$httpBackend.expectGET('/api/users/peterbe')
      .respond(200, JSON.stringify(sample_permissions));
      this.$httpBackend.flush();
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      this.$httpBackend.expectPUT('/api/users/peterbe/permissions/admin')
      .respond(201, JSON.stringify({new_data_version: 1}));

      this.scope.permission = {
        permission: 'admin',
        option_as_json: JSON.stringify({"product":["Fennec","Firefox"],"method":"POST"})
      };
      this.scope.updatePermission(this.scope.permission);
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.user.permissions.length).toEqual(2);
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.errors).toEqual({permissions:{}});
    });

    it("should should be able add a role", function() {
      this.$httpBackend.expectGET('/api/users/peterbe')
      .respond(200, JSON.stringify(sample_permissions));
      this.$httpBackend.flush();
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      this.$httpBackend.expectPUT('/api/users/peterbe/roles/new_role')
      .respond(201, JSON.stringify({new_data_version: 2}));

      new_role = {'role': 'new_role', 'data_version': 2};
      this.scope.role = new_role;
      this.scope.grantRole();
      expect(this.scope.saving).toEqual(true);
      expect(this.scope.user.roles).toEqual(sample_roles.roles);
      this.$httpBackend.flush();
      expect(this.scope.saving).toEqual(false);
      sample_roles.roles.push(new_role);
      expect(this.scope.user.roles).toEqual(sample_roles.roles);
    });


  });

});
