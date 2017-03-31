(function(angular){

  'use strict';

  angular
    .module('api.ApiGetWeightedMovingAverage',[])
    .factory('ApiGetWeightedMovingAverage', getSTLM);

  getSTLM.$inject = ['$resource', 'resourceApi', 'resourceActions'];


  function getSTLM($resource, resourceApi, resourceActions){
    return $resource(
      [resourceApi, 'ponderadas/'].join(""),
      {},
      resourceActions
    );
  }
})(angular);