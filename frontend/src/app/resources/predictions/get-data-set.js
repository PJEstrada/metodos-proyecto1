(function(angular){

  'use strict';

  angular
    .module('api.ApiGetFinanceData',[])
    .factory('ApiGetFinanceData', getFinanceDataResourceFactory);

  getFinanceDataResourceFactory.$inject = ['$resource', 'resourceApi', 'resourceActions'];


  function getFinanceDataResourceFactory($resource, resourceApi, resourceActions){
    return $resource(
      [resourceApi, 'meditions/'].join(""),
      {},
      resourceActions
    );
  }
})(angular);