angular.module('ticketmanor').service('users', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
    return {
        list: [],
        single: {},
        statuses: []
    };
  }

  var login = function(email, password){
    /* this should actually be a post request*/
    return $http.get('/rest/users/login.json').
      success(function(response) {
        $rootScope.current_user = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var logout = function(){
    /* this should actually be a post/delete request to distroy the cookies of current user*/
    return $http.get('/rest/users/logout.json').
      success(function(response) {
        $rootScope.current_user = null;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var signup = function() {
    /* this should actually be a post request for new user registration*/
    return $http.get('/rest/users/signup.json').
      success(function(response) {
        $rootScope.current_user = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }
  
// public methods
   return {
    list: {
    },
    single:{
    },
    login: login,
    logout: logout,
    signup: signup,
    model: {
      get: get_default
    }
   }
}]);
