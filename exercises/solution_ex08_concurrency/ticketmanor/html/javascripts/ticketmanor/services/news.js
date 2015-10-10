angular.module('ticketmanor').service('news', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
    return {
        list: [],
        single: {},
        statuses: []
    };
  }

  var news = function(news) {
    return $http.get('/rest/news.json?max_items=3').
      success(function(response) {
       news.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }
  
// public methods
   return {
    list: {
      get: news
    },
    single: {
    },
    model: {
      get: get_default
    }
   }
}]);
