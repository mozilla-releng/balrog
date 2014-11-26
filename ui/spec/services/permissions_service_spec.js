describe("Service: Permissions", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function(Permissions, $httpBackend) {
    this.$httpBackend = $httpBackend;
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  it('should return all users empty', inject(function(Permissions) {
    var sample_response = {users: []};
    this.$httpBackend.expectGET('/api/users')
    .respond(200, JSON.stringify(sample_response));
    Permissions.getUsers().success(function(response) {
      expect(response.users).toEqual([]);
    });
    this.$httpBackend.flush();
  }));

  it('should return all users with something', inject(function(Permissions) {
    var sample_response = {
      users: ["peterbe"],
    };
    this.$httpBackend.expectGET('/api/users')
    .respond(200, JSON.stringify(sample_response));
    Permissions.getUsers().success(function(response) {
      expect(response.users[0]).toEqual("peterbe");
    });
    this.$httpBackend.flush();
  }));

  it('should return all permissions for a user', inject(function(Permissions) {
    var sample_response = {
      "/releases/:name": {
        data_version: 1,
        options: null
      },
      "admin": {
        data_version: 1,
        options: null
      }
    };
    this.$httpBackend.expectGET('/api/users/peterbe/permissions')
    .respond(200, JSON.stringify(sample_response));
    Permissions.getUserPermissions('peterbe').then(function(response) {
      var expected_response = [
        {
          "data_version": 1,
          "options": null,
          "permission": "/releases/:name"
        },
        {
          "data_version": 1,
          "options": null,
          "permission": "admin"
        }
      ];
      expect(response).toEqual(expected_response);
    });
    this.$httpBackend.flush();
  }));

  it('should be able to add a user permission', inject(function(Permissions) {
    this.$httpBackend.expectPUT('/api/users/peterbe/permissions/admin')
    .respond(200, JSON.stringify({new_data_version: 2}));
    Permissions.addPermission('peterbe', {permission: 'admin'}, 'mytoken')
    .success(function(response) {
      expect(response).toEqual({new_data_version: 2});
    });
    this.$httpBackend.flush();
  }));

  it('should be able to update a user permission', inject(function(Permissions) {
    this.$httpBackend.expectPOST('/api/users/peterbe/permissions/admin')
    .respond(200, JSON.stringify({new_data_version: 2}));
    Permissions.updatePermission('peterbe', {permission: 'admin'}, 'mytoken')
    .success(function(response) {
      expect(response).toEqual({new_data_version: 2});
    });
    this.$httpBackend.flush();
  }));

  it('should be able to delete a user permission', inject(function(Permissions) {
    this.$httpBackend.expectDELETE(
      '/api/users/peterbe/permissions/admin?data_version=3&csrf_token=mytoken'
    )
    .respond(200, 'ok');
    var data = {
      permission: 'admin',
      data_version: 3
    };
    Permissions.deletePermission('peterbe', data, 'mytoken')
    .success(function(response) {
      expect(response).toEqual("ok");
    });
    this.$httpBackend.flush();
  }));

});
