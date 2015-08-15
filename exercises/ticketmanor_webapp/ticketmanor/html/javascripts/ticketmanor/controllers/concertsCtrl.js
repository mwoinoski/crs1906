var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('concertsCtrl',['$scope', '$rootScope', '$state', 
  'concerts', '$timeout', function($scope, $rootScope, $state, concerts, $timeout) {
  var _scope = {};
  _scope.init = function() {
    $scope.concerts_view = false;
    $scope.concerts_list = false;
    $scope.news = concerts.model.get();
    $scope.concerts = concerts.model.get();
    $scope.concerts.single.event_type = 1;
    concerts.list.get_news($scope.news);
    $rootScope.current_module = "Concerts";
    $rootScope.concerts = true;
    $rootScope.sports = false;
    $rootScope.movies = false;
    $scope.search_param = true;
    $scope.arrows = false;
    $scope.page_size = 4;
    $scope.page = 0;
    $scope.Math = window.Math;  // required to use JavaScript Math functions

    // change Artist search input's placeholder text when search term changes
    $scope.concerts_search_placeholder = "Which Artist do you want?"
    $scope.update_concerts_search_placeholder = function(code) {
      $scope.concerts_search_placeholder = "Which " + code + " do you want?"
    }

    // TODO: populate menu from JSON MW 2015-07-28
    // Add $http to arg list above
//    $scope.location_menu_options = []
//    $http.get('/rest/events/concerts/countries.json').
//      success(function(response) {
//        $scope.location_menu_options = response;
//    }).error(function(response) {
//        toastr.error('Something went wrong');
//    });
  }
  $scope.search = function(concerts_params, page, param) {
    $scope.page = page;
    if(param) {
      $scope.page = 0;
    }
    // concerts: concerts.js: first arg to angular.module('ticketmanor').service('concerts', ...
    // list: public method returned from angular.module(...)
    // search: maps to list_search
    // list_search: sends REST request
    concerts.list.search(concerts_params, $scope.concerts, $scope.page, $scope.page_size)
    .then(function(response) {
      $timeout(function() {
        $scope.concerts_view = true;
        $scope.concerts_list = true;
      }, 800);
      $scope.page += 1;
    });
  }
  _scope.init();
}]);