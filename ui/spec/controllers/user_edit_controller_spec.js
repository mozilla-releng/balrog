
describe("controller: UserPermissionsCtrl", function() {

  beforeEach(function() {
    module("app");
  });

  var user = {
    username: "peterbe"
  };

  var sample_permissions = {
    "/releases/:name": {
      data_version: 1,
      options: null
    }
  };

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
      users: [user],
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the edit rule modal", function() {

    it("should should all defaults", function() {
      this.$httpBackend.expectGET('/api/users/peterbe/permissions')
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
        ]
      });
      // expect(this.scope.user.username).toEqual('peterbe');
      expect(this.scope.is_edit).toEqual(true);
    });
    //
    it("should should be able add a permission", function() {
      this.$httpBackend.expectGET('/api/users/peterbe/permissions')
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
      this.$httpBackend.expectGET('/api/users/peterbe/permissions')
      .respond(200, JSON.stringify(sample_permissions));
      this.$httpBackend.flush();
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      this.$httpBackend.expectPOST('/api/users/peterbe/permissions/admin')
      .respond(201, JSON.stringify({new_data_version: 1}));

      this.scope.permission = {
        permission: 'admin',
        option_as_json: JSON.stringify({"product":["Fennec","Firefox"],"method":"POST"})
      };
      this.scope.updatePermission(this.scope.permission);
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.user.permissions.length).toEqual(1);
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.errors).toEqual({permissions:{}});
    });

  });

});
