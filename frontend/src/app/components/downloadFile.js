(function(angular){

  angular
    .module('frontend.common.downloadFiles', [])
    .service('DownloadFile', downloadFileService);

  downloadFileService.$inject = ['$window', '$document'];

  function downloadFileService($window, $document){
    var vm = this;

    vm.download = function(byteBody, contentType, fileNameWithExtension){

      // Create data from bytes
      var arrayBufferView = new Uint8Array(byteBody);
      var file = new Blob( [arrayBufferView], {type: contentType});

      // Dynamically create linked tag to blob
      var link = $document[0].createElement('a');
      link.href = $window.URL.createObjectURL(file);
      link.download =  fileNameWithExtension;
      link.click();
    }
  }
})(angular);