// from http://uncorkedstudios.com/blog/multipartformdata-file-upload-with-angularjs
angular.module('app').directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

// angular.module('app').service('fileUpload', ['$http', function ($http) {
//     this.uploadFileToUrl = function(file, uploadUrl){
//         var fd = new FormData();
//         fd.append('file', file);
//         $http.post(uploadUrl, fd, {
//             transformRequest: angular.identity,
//             headers: {'Content-Type': undefined}
//         })
//         .success(function(){
//         })
//         .error(function(){
//         });
//     };
// }]);


angular.module('app').controller('NewReleaseCtrl',
function($scope, $http, $modalInstance, CSRFService, ReleasesService, releases) {

  $scope.releases = releases;
  $scope.release = {
    name: 'winterfox-nightly-2014',//XXX HACK
    product: 'Winterfox',
    version: '99.' + Math.round(Math.random()*10, 1),
  };
  $scope.errors = {};
  $scope.saving = false;

  $scope.saveChanges = function () {
    if (!$scope.release.product.trim()) {
      alert('Product is a minimum');
      return;
    }
    $scope.saving = true;
    $scope.errors = {};
    CSRFService.getToken()
    .then(function(csrf_token) {

      var file = $scope.dataFile;
      var fd = new FormData();
      fd.append('data', file);
      fd.append('name', $scope.release.name);
      fd.append('product', $scope.release.product);
      fd.append('version', $scope.release.version);

      // $http.post('/api/releases', fd, {
      // // $http.post('http://requestb.in/qe1wlsqe', fd, {
      //     // transformRequest: angular.identity,
      //     // headers: {'Content-Type': undefined}
      //     headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      // })
      $http({
          method: 'POST',
          url: '/api/releases',
          data: fd,
          transformRequest: angular.identity,
          headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      })
      .success(function(response){
        console.log(response);
      })
      .error(function(){
        console.error(arguments);
      });

      // fileUpload.uploadFileToUrl('/api/releases', );

      // release = angular.copy($scope.release);
      // ReleasesService.addRelease(release, csrf_token)
      // .success(function(response) {
      //   $scope.release.data_version = 1;
      //   console.log("RESP(ONSE)", response);
      //   $scope.release.id = parseInt(response, 10);
      //   $scope.releases.push($scope.release);
      //   $modalInstance.close();
      // }).error(function(response, status) {
      //   if (typeof response === 'object') {
      //     $scope.errors = response;
      //     sweetAlert(
      //       "Form submission error",
      //       "See fields highlighted in red.",
      //       "error"
      //     );
      //   }
      // }).finally(function() {
      //   $scope.saving = false;
      // });

    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
