(function() {
  'use strict';

  angular
    .module(
      'frontend',
      [
        'ngAnimate',
        'ngSanitize',
        'ngResource',
        'ui.router',
        'weed',
        'frontend.api',
        'frontend.common',
        'frontend.interceptors',
        'ngFileUpload',
        'chart.js',
        '720kb.datepicker',
      ]);

})();
