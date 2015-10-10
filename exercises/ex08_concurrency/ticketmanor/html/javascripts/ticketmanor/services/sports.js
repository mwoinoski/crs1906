angular.module('ticketmanor').service('sports', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
    return {
        list: [],
        single: {},
        statuses: []
    };
  }

  var news = function(news_id, news) {
//    return $http.get('/rest/events/sports/news/1.json',{news_id: news_id}).  //MW 2015-07-28
    return $http.get('/rest/news/sports/' + news_id + '.json').
      success(function(response) {
      news.single = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var list_news = function(news) {
    return $http.get('/rest/news/sports.json', {params: {max_items: 10}}).  //MW 2015-07-28
      success(function(response) {
       news.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

   var list_search = function(sports_params, sports, page, page_size) {
    return $http.get('/rest/events/sports/list.json?page=page&page_size=page_size', {params: sports_params.single}).
      success(function(response) {
        sports.list.events_length = response.events.length;
        if(page == 0) {
          sports.list.page_back = page;
        } else {
          sports.list.page_back = page-1;
        }
        sports.list.events = response.events.splice(page*page_size, page_size);
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var event = function(event_id, event) {
    return $http.get('/rest/events/sports/1.json',{event_id: event_id}).
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
