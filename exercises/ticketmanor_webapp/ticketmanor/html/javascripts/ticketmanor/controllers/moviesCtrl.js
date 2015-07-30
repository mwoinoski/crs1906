var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('moviesCtrl',['$scope', '$rootScope', '$state', 'movies', '$timeout',
  function($scope, $rootScope, $state, movies, $timeout) {
  var _scope = {};
  _scope.init = function() {
    $scope.movies_view = false;
    $scope.movies_list = false;
    $scope.news = movies.model.get();
    $scope.movies = movies.model.get();
    movies.list.get_news($scope.news);
    $rootScope.current_module = "Movies";
    $rootScope.movies = true;
    $rootScope.concerts = false;
    $rootScope.sports = false;
    $scope.search_param = true;
    $scope.arrows = false;
    $scope.page_size = 6;
    $scope.page = 0;

    // change Movies search input's placeholder text when search term changes
    $scope.movies_search_placeholder = "Which Movie do you want?"
    $scope.update_movies_search_placeholder = function(code) {
      $scope.movies_search_placeholder = "Which " + code + " do you want?"
    }

  }

  $scope.search = function(sports_params, page, param) {
    $scope.page = page;
    if(param) {
      $scope.page = 0;
    }
    movies.list.search(sports_params, $scope.movies, $scope.page, $scope.page_size)
      .then(function(response) {
        $timeout(function() {
          $scope.movies_view = true;
          $scope.movies_list = true;
        }, 800);
      });
    $scope.page += 1;
  } 

  _scope.init();
}]);