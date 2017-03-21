(function (angular) {
  'use strict';

  angular
    .module('frontend.common.manageEnter', [])
    .directive('ngEnter', ngEnter);

  ngEnter.$inject = ['$log'];
  function ngEnter($log) {
    return function(scope, element, attrs) {
        element.bind("keydown keypress", function(event) {
            if(event.which === 13) {
                scope.$apply(function(){
                    scope.$eval(attrs.ngEnter, {'event': event});
                });

                event.preventDefault();
            }
        });
    };
  }
})(angular);
