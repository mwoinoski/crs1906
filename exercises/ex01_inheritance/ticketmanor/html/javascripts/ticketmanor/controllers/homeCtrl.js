var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('homeCtrl',['$scope', '$rootScope', '$state', 'movies', '$timeout',
  function($scope, $rootScope, $state, movies, $timeout) {
  var _scope = {};
  _scope.init = function() {
    $rootScope.current_module = false;
    $scope.home_nav_margin = true;
  }  
  _scope.init();
}]);