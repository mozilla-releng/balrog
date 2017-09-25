angular.module('app').directive("permissionOptions", [function(){
    return {
        restrict: 'E',
        scope: {
            permission: '='
        },
        template: ' <div class="form-group" ng-class="{\'has-error\': errors.options_as_json}"> '+
'    <label>Options</label>'+
'    <div class="dropdown">'+
'        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">'+
'            <span ng-if="!selected_options.length">Select Options</span>'+
'            <span ng-if="!!selected_options.length">'+
'                {{ selected_options.join(\' | \') }}'+
'            </span>'+
'            <span class="caret"></span></button>'+
'        <ul class="dropdown-menu" ng-click="$event.stopPropagation();">'+
'            <label ng-hide="!!available_options.length" class="col-sm-12">Please select a permission</label>'+
'            <li ng-repeat="option in available_options"><Label class="col-sm-12"><input ng-click="toggleOption(option)" type="checkbox" ng-checked="!!(selected_options.indexOf(option)+1)"> &nbsp;{{option}}</Label></li>'+
'        </ul>'+
'    </div>'+
'    <p class="help-block" ng-show="errors.options">{{ errors.options.join(\', \') }}</p>'+
'</div>'+
'<div class="form-group" ng-show="!!(selected_options.indexOf(\'actions\')+1)">'+
'    <label><i>actions</i></label>'+
'    <div class="row-fluid m-tag__input">'+
'        <label ng-repeat="action in selected_actions" class="btn btn-sm btn-warning">{{ action }} <span class="badge" ng-click="actionRemove(action)">x</span></label>'+
'        <input type="text" typeahead="action for action in actions[permission.permission] | filter:$viewValue | limitTo:16" ng-model="action"></input>'+
'    </div>'+
'</div>'+
'<div class="form-group" ng-show="!!(selected_options.indexOf(\'products\')+1)">'+
'    <label><i>products</i></label>'+
'    <div class="row-fluid m-tag__input">'+
'        <label ng-repeat="product in selected_products" class="btn btn-sm btn-primary">{{ product }} <span class="badge" ng-click="productRemove(product)">x</span></label>'+
'        <input type="text" typeahead="product for product in products | filter:$viewValue | limitTo:16" ng-model="product"></input>'+
'    </div>'+
'</div> ',
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

            $scope.$watch('[ action, product ] | json',function(){
                // add tag on action input
                if ($scope.actions[$scope.permission.permission].indexOf($scope.action) !== -1 && $scope.selected_actions.indexOf($scope.action) === -1){
                    $scope.selected_actions.push($scope.action);
                    $scope.action = null;
                }

                // add tag on product input
                if($scope.products.indexOf($scope.product) !== -1 && $scope.selected_products.indexOf($scope.product) === -1){
                    $scope.selected_products.push($scope.product);
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
