(function() {
  'use strict';

  angular
    .module('frontend')
    .controller('MainController', mainController);

  mainController.$inject = ['$state'];
  
  function mainController($state) {
    var vm = this;
    vm.states = $state.get();
  }
})();
