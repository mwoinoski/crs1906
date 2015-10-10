angular.module('ticketmanor').service('chat', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
    return {
        list: [],
        single: {},
        statuses: []
    };
  }
  
  var chat_list = function(welcome_params, chat) {
    return $http.get('/rest/events/chat/list.json', {welcome_params: welcome_params}).
      success(function(response) {
       chat.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var send = function(chat, message, short_name) {
    return $http.get('/rest/events/chat/list.json',{message: message, short_name: short_name}).
      success(function(response) {
       chat.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var invite_friend = function(email, chat) {
    return $http.get('/rest/events/chat/invite.json',{email: email}).
    success(function(response) {
      chat.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }
// public methods
   return {
    list: {
      get: chat_list
    },
    single: {
      post: send,
      invite: invite_friend
    },
    model: {
      get: get_default
    }
   }
}]);
