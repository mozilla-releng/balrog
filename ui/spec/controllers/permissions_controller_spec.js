describe("controller: PermissionsController", function() {

  beforeEach(function() {
    module("app");
  });

  var empty_user = '';

  var sample_users = {
    peterbe: {
      roles: [
        { 'role': 'qa', 'data_version': 1 },
        { 'role': 'releng', 'data_version': 1 }
      ]
    },
    bhearsum: {
      roles: [
        { 'role': 'qa', 'data_version': 1 },
        { 'role': 'releng', 'data_version': 1 }
      ]
    }
  };

  var sample_permissions = {
    "/releases/:name": {
      data_version: 1,
      options: null
    },
    "admin": {
      data_version: 1,
      options: null
    }
  };

    var sample_roles = {
    'roles': [
      {'role':'qa', 'data_version': 1},
      {'role':'releng', 'data_version':1}
    ]};
  var sample_all_roles = {'roles': ['qa', 'releng']};

  beforeEach(inject(function($controller, $rootScope, $location, Permissions, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('PermissionsController', {
      $scope: this.scope,
      $location: $location,
      Permissions: Permissions
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching all users", function() {
    it("should return all rules empty", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, '{}');
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, '{"required_signoffs": []}');
      this.$httpBackend.flush();
      expect(this.scope.users).toEqual([]);
    });

    it("should return all rules some", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, JSON.stringify(sample_users));
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, '{"required_signoffs": []}');
      this.$httpBackend.flush();
      expect(this.scope.users.length).toEqual(2);
      expect(this.scope.users).toEqual([
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
        }]);
    });

  });

  describe("filter by search", function() {
    it("should return true always if no filters active", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, '{}');
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, '{"required_signoffs": []}');
      this.$httpBackend.flush();

      var item = {
        username: "peterbe",
      };
      expect(this.scope.filterBySearch(item)).toEqual(true);
    });

    it("should filter when only one search word name", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, '{}');
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, '{"required_signoffs": []}');
      this.$httpBackend.flush();

      var $scope = this.scope;
      $scope.filters.search = "pet";
      $scope.$apply();
      var item = {
        username: "peterbe",
      };
      expect($scope.filterBySearch(item)).toEqual(true);
      item.username = "seinfeld";
      expect($scope.filterBySearch(item)).toEqual(false);
    });

    it("should notice if filters are on", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, JSON.stringify(sample_users));
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, '{"required_signoffs": []}');
      this.$httpBackend.flush();

      var $scope = this.scope;
      expect($scope.hasFilter()).toEqual(false);
      $scope.filters.search = 'something';
      $scope.$apply();
      expect($scope.hasFilter()).toEqual(true);
    });
  });

  describe('opening modals', function() {
    it("should be possible to open the add modal", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, JSON.stringify(sample_users));
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, JSON.stringify(sample_all_roles));
      this.$httpBackend.expectGET('/api/releases/columns/product').respond(200,{});
      this.scope.openNewModal();
    });

    it("should be possible to open the edit modal", function() {
      this.$httpBackend.expectGET('/api/users')
      .respond(200, JSON.stringify(sample_users));
      this.$httpBackend.expectGET('/api/required_signoffs/permissions')
      .respond(200, '{"required_signoffs": []}');
      this.$httpBackend.expectGET('/api/users/peterbe')
      .respond(200, JSON.stringify(sample_permissions));
      this.$httpBackend.expectGET('/api/releases/columns/product').respond(200,{});
      this.scope.openUpdateModal({username: "peterbe"});
    });
  });

});


describe("controller: PermissionsController by username", function() {

  beforeEach(function() {
    module("app");
  });

  var sample_permissions = {
    "permissions": {
      "/releases/:name": {
        data_version: 1,
        options: null
      },
      "admin": {
        data_version: 1,
        options: null
      }
    },
    "roles": {}
  };

  beforeEach(inject(function($controller, $rootScope, $location, Permissions, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('PermissionsController', {
      $scope: this.scope,
      $location: $location,
      Permissions: Permissions,
      $routeParams: {username: "peterbe"}
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching specific permissions", function() {

    it("should return all permissions by username", function() {
      inject(function($route, $location, $rootScope) {

        expect($route.current).toBeUndefined();
        this.$httpBackend.expectGET('/api/users/peterbe')
        .respond(200, JSON.stringify(sample_permissions));
        this.$httpBackend.expectGET('/api/required_signoffs/permissions')
        .respond(200, '{"required_signoffs": []}');

        $location.path('/permissions/peterbe');
        $rootScope.$digest();
        expect($route.current.controller).toEqual('PermissionsController');

        this.$httpBackend.flush();
        var $scope = this.scope;
        expect($scope.permissions.length).toEqual(2);
        expect($scope.permissions).toEqual([
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
        ]);
      });
    });
  });

});
