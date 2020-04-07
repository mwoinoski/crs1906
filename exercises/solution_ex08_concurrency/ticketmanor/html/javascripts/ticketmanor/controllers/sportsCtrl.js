var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('sportsCtrl',['$scope', '$rootScope', '$state', 'sports', '$timeout',
  function($scope, $rootScope, $state, sports, $timeout) {
  var _scope = {};
  _scope.init = function() {
    $scope.sports_view = false;
    $scope.sports_list = false;
    $scope.news = sports.model.get();
    $scope.sports = sports.model.get();
    sports.list.get_news($scope.news);
    $rootScope.current_module = "Sports";
    $rootScope.sports = true;
    $rootScope.concerts = false;
    $scope.search_param = true;
    $scope.arrows = false;
    $scope.page_size = 4;
    $scope.page = 0;

    $scope.sports_search_placeholder = "Which Event, team, or athlete do you want?"
    $scope.update_sports_search_placeholder = function(code) {
      $scope.sports_search_placeholder = "Which " + code + " do you want?"
    }

  } 
  $scope.search = function(sports_params, page, param) {
    $scope.page = page;
    if(param) {
      $scope.page = 0;
    }
    sports.list.search(sports_params, $scope.sports, $scope.page, $scope.page_size)
      .then(function(response) {
        $timeout(function() {
          $scope.sports_view = true;
          $scope.sports_list = true;
        }, 800);
      });
    $scope.page += 1;
  } 
  _scope.init();
}]);