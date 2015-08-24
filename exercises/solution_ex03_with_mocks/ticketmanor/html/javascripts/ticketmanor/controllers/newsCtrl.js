var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('newsCtrl',['$scope', '$rootScope', '$state', 
  '$stateParams', '$timeout', 'concerts', 'sports', 'movies',
  function($scope, $rootScope, $state, $stateParams, $timeout, concerts, sports, movies) {
  var _scope = {};
  _scope.init = function() {
    $scope.event_type = $stateParams.event_type;
    if($stateParams.event_type == 'concerts') {
      $scope.news = concerts.model.get();
      concerts.single.get_news($stateParams.news_id, $scope.news);
    } 
    else if($stateParams.event_type == 'sports') {
      $scope.news = sports.model.get();
      sports.single.get_news($stateParams.news_id, $scope.news);
    }
    else if($stateParams.event_type == 'movies'){
      $scope.news = movies.model.get();
      movies.single.get_news($stateParams.news_id, $scope.news);
    }
  }  
  _scope.init();
}]);