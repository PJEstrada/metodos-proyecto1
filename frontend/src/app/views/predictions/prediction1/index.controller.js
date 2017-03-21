(function(angular) {
  'use strict';

  // Module fetch
  angular
    .module('frontend')
    .controller(
      'PredictionController',
      predictionController);

  predictionController.$inject = [
    '$scope',
    '$stateParams',
    '$log',
    '$state',
    'WeedApi',
    'moment',
    'ApiGetPredictions'
  ];
  function predictionController(
    $scope,
    $stateParams,
    $log,
    $state,
    WeedApi,
    moment,
    ApiGetPredictions
  ) {
    var vm = this;
    vm.display_mode = "date";
    // Initial end time is current hour
    vm.endTime = new Date();
    vm.endTimeHours = new Date();
    // Set format for HTML input field
    vm.endTimeInput = moment(vm.endTime).format("HH:mm");
    // Set initial hour as curent hour minus 1 hour
    vm.initialTime = new Date();
    vm.initialTimeHours = new Date();
    vm.initialTime.setDate(vm.initialTime.getDate() - 1);
    vm.initialTimeHours.setDate(vm.initialTimeHours.getDate() - 1);
    // Set format for HTML input field
    vm.initialTimeInput = moment(vm.initialTime).format("HH:mm");
    vm.newDataset = {};

    vm.uploadDataset = function(){
      $log.log(vm.newDataset);
      ApiGetPredictions.save(vm.newDataset);
      $log.log("upload called");
    };

    // Fetch All predictions
    vm.fetchMeterData = function () {
      vm.data = [];
      vm.data.push({x: new Date(), y:10 });
      vm.data.push({x: new Date(), y: 12});
      vm.data.push({x: new Date(), y: 15});
      /*new ApiGetMeter.get({id: $stateParams.id})
        .$promise.then(function (response) {
        vm.meter = response.data;

      }, function (err) {

      }).then(function () {
        // Prepare request to get entries.
        vm.entries = new ApiGetEntries();
        // Add paremeters
        vm.entries.begin_date = moment(vm.initialTime).format("YYYY-MM-DDTHH:mm:ssZ");
        vm.entries.end_date = moment(vm.endTime).format("YYYY-MM-DDTHH:mm:ssZ");

        vm.entries.$save(function (response) {
          $log.log(response);
          var dataPoints = response.data;
          vm.currentEntries = [];
          vm.logEntries = [];
          for (var i = 0; i < dataPoints.length; i++) {
            // Parse the received date
            var dateReceived = dataPoints[i].inserted_at;
            var dateObject = new Date(dateReceived);
            // Extract the fuel level (sonar) and the date and time
            vm.currentEntries.push(
              {
                'time': dateObject,
                'level': dataPoints[i].sonnar
              }
            );

            // Adding log entries for right side log display.
            vm.logEntries.push(
              {
                'time': dateObject,
                'level': dataPoints[i].sonnar,
                'temperature': dataPoints[i].temperature
              }
            );
          }
          $log.log("new first: ", vm.currentEntries[0]);
          var filteredData = getAveragesEntries(vm.currentEntries, 5);
          //$log.log("AVERAGED: ",vm.currentEntries);
          // Refreshing graph
          vm.data = [];
          // Setting time scale (x axis)

          for (var i = 0; i < filteredData.length; i++) {
            vm.data.push(
              {
                x: filteredData[i].time,
                y: filteredData[i].level
              }
            )
          }
          vm.data.sort(function (a, b) {
            // Turn your strings into dates, and then subtract them
            // to get a value that is either negative, positive, or zero.
            return new Date(b.x) - new Date(a.x);
          });

          $log.log("DATA", vm.data);
          vm.updateChartOptions();
        }, function (err) {
          $log.log(err);
        });


      });*/
    };

    vm.refreshGrid = function(){
      if(vm.display_mode == 'hours'){
        var hours = vm.endTimeHours.getHours();
        var minutes = vm.endTimeHours.getMinutes();
        vm.endTime.setHours(hours);
        vm.endTime.setMinutes(minutes);
        var hoursInit = vm.initialTimeHours.getHours();
        var minutesInit = vm.initialTimeHours.getMinutes();
        vm.initialTime.setHours(hoursInit);
        vm.initialTime.setMinutes(minutesInit);
        vm.updateChartOptions();
      }
      else{
        vm.updateChartOptions();
      }

    }
    function arrayMin(arr) {
      return arr.reduce(function (p, v) {
        return ( p < v ? p : v );
      });
    }

    function arrayMax(arr) {
      return arr.reduce(function (p, v) {
        return ( p > v ? p : v );
      });
    }

    vm.changeInputs = function(){


    };
    /*
     * This function updates the axis on the chart so it
     * reflects any new data it has received.
     * */
    vm.updateChartOptions = function (){
      // Get the min and max levels of the current data
      if(vm.display_mode == 'hours'){
        vm.options = {
          type:'line',
          fill: false,
          backgroundColor: 'transparent',
          scales: {
            xAxes: [{
              type:"time",
              time:{
                unit:'hour',
                min: vm.initialTime,
                max: vm.endTime
              },
              position: 'bottom'
            }]
          }
        };
      }
      else{
        vm.options = {
          type:'line',
          fill: false,
          backgroundColor: 'transparent',
          scales: {
            xAxes: [{
              type:"time",
              time:{
                unit:'day',
                min: vm.initialTime,
                max: vm.endTime
              },
              position: 'bottom'
            }]
          }
        };
      }

    };

    function getAveragesEntries(data, divisor){
      var initTime = new Date(vm.initialTime.getTime());
      var dateList = [];
      var endTime = new Date(vm.endTime.getTime());
      var currentTime = new Date(vm.initialTime.getTime());
      var i = 0;
      var result = [];
      while(currentTime < endTime){
        // Add minutes divisor
        currentTime.setMinutes(currentTime.getMinutes()+divisor);

        // Filter dates between current time and previous time
        var timeA = -1;
        var timeB = currentTime;
        if (dateList==0){
          // If is the first iteration, use initial time
          timeA = initTime;
        }
        else{
          // Else, use the previous time
          timeA = dateList[i-1];
        }
        // Save new interval
        dateList.push(new Date(currentTime.getTime()));
        var filteredData = filterDates(data,timeA,timeB);
        if (filteredData == 0){
          // If there are now plots on the interval, try to get the previous input
          if(result.length > 0){
            averageLevel = result[i-1].level;
            result.push({'time': currentTime, 'level': averageLevel});
          }
          else{
            result.push({'time': currentTime, 'level': undefined});
          }

        }
        // If we have data in the interval
        else{
          // Calculate Average
          var averageLevel = 0;
          for(var j = 0; j<filteredData.length; j++){
            averageLevel += filteredData[j].level;
          }
          averageLevel = averageLevel/filteredData.length;
          result.push({'time': new Date(currentTime.getTime()), 'level': averageLevel});
        }

        i++;
      }
      return result;

    }

    /**
     *
     * Filter dates between the dates a and b
     * list is a json of the form {'level': xx, 'time': xx}
     * @param a
     * @param b
     */
    function filterDates(list, a, b){
      var result = [];
      for(var i=0; i < list.length; i++){
        if(list[i].time >= a && list[i].time<=b){
          result.push(list[i]);
        }
      }
      return result;
    }

    vm.fetchMeterData();
  }
})(angular);
