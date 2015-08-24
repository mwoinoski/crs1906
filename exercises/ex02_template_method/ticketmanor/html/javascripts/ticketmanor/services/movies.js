angular.module('ticketmanor').service('movies', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
    return {
        list: [],
        single: {},
        statuses: []
    };
  }

  var news = function(news_id, news) {
//    return $http.get('/rest/events/movies/news/1.json', {news_id: news_id}).  //MW 2015-07-28
    return $http.get('/rest/news/movies/' + news_id + '.json').
      success(function(response) {
      news.single = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var list_news = function(news) {
    return $http.get('/rest/news/movies.json', {params: {max_items: 10}}).  //MW 2015-07-28
      success(function(response) {
       news.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var list_search = function(movies_params, movies, page, page_size) {
    return $http.get('/rest/events/movies/list.json?page=page&page_size=page_size', {params: movies_params.single}).
      success(function(response) {
        movies.list.events_length = response.events.length;
        if(page_size == 0) {
          movies.list.page_back = page;
        } else {
          movies.list.page_back = page-1;
        }
        movies.list.events = response.events.splice(page*page_size, page_size);
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var event = function(event_id, event) {
    return $http.get('/rest/events/movies/1.json',{event_id: event_id}).
      success(function(response) {
      event.single = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }
  
// public methods
   return {
    list: {
      get_news: list_news,
      search: list_search
    },
    single:{
      get_news: news,
      get_event: event
    },
    model: {
      get: get_default
    }
   }
}]);
