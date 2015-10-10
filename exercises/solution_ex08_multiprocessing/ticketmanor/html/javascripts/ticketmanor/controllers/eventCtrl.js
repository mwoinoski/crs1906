var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('eventCtrl',['$scope', '$rootScope', '$state', 
  '$stateParams', '$timeout', 'concerts', 'sports', 'movies',
  function($scope, $rootScope, $state, $stateParams, $timeout, concerts, sports, movies) {
  var _scope = {};
  _scope.init = function() {
    $rootScope.chat_button = false;
    $scope.event_type = $stateParams.event_type;
    if($stateParams.event_type == 'concerts') {
      $scope.event = concerts.model.get();
      concerts.single.get_event($stateParams.event_id, $scope.event);
    } 
    else if($stateParams.event_type == 'sports') {
      $scope.event = sports.model.get();
      sports.single.get_event($stateParams.event_id, $scope.event);
    }
    else if($stateParams.event_type == 'movies'){
      $scope.event = movies.model.get();
      movies.single.get_event($stateParams.event_id, $scope.event);
    }
  }  
  _scope.init();
}]);