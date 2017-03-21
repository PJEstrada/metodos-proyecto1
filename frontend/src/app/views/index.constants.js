/**
 * Created by venator on 6/2/16.
 */
(function(angular) {
  'use strict';

  // Module fetch
  angular
    .module('frontend')
    .constant('resourceActions', {
      update: {
        method: 'PUT'
      },
      query: {
        isArray: false
      }
    })
    .constant('resourceApi', 'http://localhost:8000/api/');

})(angular);
