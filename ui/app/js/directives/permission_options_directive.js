angular.module('app').directive("permissionOptions", [function(){
    return {
        restrict: 'E',
        scope: {
            permission: '='
        },
        templateUrl: 'permission_options.html' ,
        controller: function($scope, Releases){
            var allPermissions = {
                "admin": ["products"],
                "release": ["actions", "products"],
                "release_locale": ["actions", "products"],
                "release_read_only": ["actions", "products"],
                "rule": ["actions", "products"],
                "permission": ["actions"],
                "required_signoff": ["products"],
                "scheduled_change": ["actions"],
            };
            $scope.$watch('permission.permission',function(){
                $scope.available_options = allPermissions[$scope.permission.permission];

                // clear  all previous selections 
                $scope.selected_options = [];
                $scope.selected_actions = [];
                $scope.selected_products = [];
            });
            $scope.selected_options = [];
            $scope.actions = {
                "admin": [],
                "rule": ["create", "modify", "delete"],
                "release": ["create", "modify", "delete"],
                "release_read_only": ["set", "unset"],
                "release_locale": ["modify"],
                "required_signoff": ["create", "modify", "delete"],
                "permission": ["create", "modify", "delete"],
                "scheduled_change": ["enact"],
                "":[]
            };

            $scope.selected_actions = [];
            $scope.action = null;

            $scope.products = [];
            $scope.selected_products = [];
            $scope.product = null;

            // get products in releases
            Releases.getProducts().success(function(response) {
                $scope.products = response.product;
            });

            // monitor for changes in action or product value
            $scope.$watch('[ action, product ] | json',function(){
                // add tag for action when terminated with comma
                if ($scope.action && $scope.action.indexOf(",") !== -1 && $scope.action.trim().length > 1){
                    var action = $scope.action.slice(0, -1).trim();
                    // do not add duplicates to the selected
                    if($scope.selected_actions.indexOf(action) === -1){
                        $scope.selected_actions.push(action);
                    }
                    $scope.action = null;
                }

                // add tag for product when terminated with comma
                if ($scope.product && $scope.product.indexOf(",") !== -1 && $scope.product.trim().length > 1){
                    var product = $scope.product.slice(0, -1).trim();
                    // do not add duplicates to the selected
                    if($scope.selected_products.indexOf(product) === -1){
                        $scope.selected_products.push(product);
                    }
                    $scope.product = null;
                }

                if($scope.selected_options.indexOf('actions') === -1){
                    $scope.selected_actions = [];
                }
                if($scope.selected_options.indexOf('products') === -1){
                    $scope.selected_products = [];
                }

                // always update options_as_json according to selected tags
                var options = {};
                if ($scope.selected_products.length > 0 ) { options["products"] = $scope.selected_products; } 
                if ($scope.selected_actions.length > 0) { options["actions"] = $scope.selected_actions; } 
                $scope.permission.options_as_json = JSON.stringify(options);
            });

            $scope.actionRemove = function(action){
                $scope.selected_actions.splice($scope.selected_actions.indexOf(action), 1);
            };

            $scope.productRemove = function(product){
                $scope.selected_products.splice($scope.selected_products.indexOf(product), 1);
            };

            $scope.toggleOption = function(option){
                if($scope.selected_options.indexOf(option) !== -1){
                    $scope.selected_options.splice($scope.selected_options.indexOf(option), 1);
                }else{
                    $scope.selected_options.push(option);
                }
            };

        }

    };
}]);
