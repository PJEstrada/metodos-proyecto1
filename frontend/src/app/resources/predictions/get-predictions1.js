(function(angular){

  'use strict';

  angular
    .module('api.ApiGetPredictions',[])
    .factory('ApiGetPredictions', getAllMetersResourceFactory);

  getAllMetersResourceFactory.$inject = ['$resource', 'resourceApi', 'resourceActions'];


  function transformRequest(data) {
    if (data === undefined)
      return data;

    var fd = new FormData();
    angular.forEach(data, function(value, key) {
      if (value instanceof FileList) {
        if (value.length == 1) {
          fd.append(key, value[0]);
        } else {
          angular.forEach(value, function(file, index) {
            fd.append(key + '_' + index, file);
          });
        }
      } else {
        fd.append(key, value);
      }
    });

    return fd;
  };
  function getAllMetersResourceFactory($resource, resourceApi, resourceActions){
    return $resource(
      [resourceApi, 'dataset/:pk'].join(""),
      {'pk': '@pk'},
      {
        'save':{
          'method': 'POST',
          'transformRequest': transformRequest,
          'headers': {'Content-Type': undefined}
        }
      }
    );
  }
})(angular);