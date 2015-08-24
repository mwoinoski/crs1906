var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('AuthCtrl',['$scope', '$rootScope', '$state', 'users', '$timeout',
  function($scope, $rootScope, $state, users, $timeout) {
  var _scope = {};
  _scope.init = function() {
    $rootScope.chat_button = false;
    $rootScope.current_module = false;
    $scope.events = [];
    $timeout(function(){
      $scope.show_background = true;
      $scope.show_header = true;        
      $timeout(function(){
        $scope.show_content = true;
        $timeout(function(){
          $scope.set_events();
          $scope.show_copy_right = true; 
        }, 500);
      }, 500);
    }, 100);
  }
  $scope.login = function(credentials) {
    users.login(credentials.email, credentials.password).then(function(response){
      if( $rootScope.view_cart) {
        $state.go('events.show.checkout');
      } else {
        $state.go('root.home');
      }
    });
  }
  $scope.logout = function() {
    users.logout().then(function(response){
      $state.go('root.home');
    });
  }
  $scope.signup = function(signup_paramas) {
   users.signup(signup_paramas).then(function(response){
      $state.go('root.home');
    });
  }
  $scope.set_events = function() {
    $scope.events= [{name: 'Concerts', ui_state: 'events.show.concerts', icon: 'fa fa-music'},
                    {name: 'Sports', ui_state: 'events.show.sports', icon: 'fa fa-futbol-o'}, 
                    {name: 'Movies', ui_state: 'events.show.movies', icon: 'fa fa-film'}]  
  }
  
  _scope.init();
}]);