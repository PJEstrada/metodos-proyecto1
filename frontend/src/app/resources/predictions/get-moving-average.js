(function(angular){

  'use strict';

  angular
    .module('api.ApiGetMovingAverage',[])
    .factory('ApiGetMovingAverage', getSTLM);

  getSTLM.$inject = ['$resource', 'resourceApi', 'resourceActions'];


  function getSTLM($resource, resourceApi, resourceActions){
    return $resource(
      [resourceApi, 'analisis/'].join(""),
      {},
      resourceActions
    );
  }
})(angular);