(function(angular){

  'use strict';

  angular
    .module('api.ApiGetSTLM',[])
    .factory('ApiGetSTLM', getSTLM);

  getSTLM.$inject = ['$resource', 'resourceApi', 'resourceActions'];


  function getSTLM($resource, resourceApi, resourceActions){
    return $resource(
      [resourceApi, 'predictions-stlm/'].join(""),
      {},
      resourceActions
    );
  }
})(angular);