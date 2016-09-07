// Note: Using 'var' in web browsers for now for cross-browser compatability
'use strict';

(() => {
  // Define global chart settings/options
  Chart.defaults.global.responsive = true;

  // Animations look bad with the charts updating on every input because
  // the unchanged chart is still reset and reanimates - just turn it off
  Chart.defaults.global.animation = false;

  var options = {
    scaleOverride: true,
    // Number - The number of steps in a hard coded scale
    scaleSteps: 10,
    // Number - The value jump in the hard coded scale
    scaleStepWidth: 10,
    // Number - The scale starting value
    scaleStartValue: 0,
  };

  // Just some blank chart data so we can initialize the charts - don't modify
  var blankData = {
    labels: [],
    datasets: [{}]
  };

  // Just a global counter so we can get a unique identifier
  var counter = 0;

  // Remembers if hw or test is empty
  var testCount = 0;
  var hwCount = 0;

  // Grab domain objects
  var hwChartElement = document.getElementById('hw-chart');
  var testChartElement = document.getElementById('test-chart');

  // Initialize the charts
  var hwCtx = hwChartElement.getContext('2d');
  var hwChart = new Chart(hwCtx).Line(blankData, options);
  var testCtx = testChartElement.getContext('2d');
  var testChart = new Chart(testCtx).Line(blankData, options);

  // Hook up some event handlers
  /* TODO */
  document.getElementById('add-hw-btn').onclick = function() {add('hw');};
  document.getElementById('add-test-btn').onclick = function() {add('test');};
  document.getElementById('hw-weight').onchange =
    function() {updatedHwWeight();};
  document.getElementById('test-weight').onchange =
    function() {updatedTestWeight();};

  /**
   * Gathers all current data from the DOM and updates the statistics.
   *
   * Grabs all hw and test items from the dom lists, then computes then
   * average for each and final grade based on the weights.
   * It then uses the values collected to generate new, updated charts.
   *
   * @return {undefined} No return
   */
  function updateStats() {
    var hwValues = [];
    var testValues = [];
    var hwData = blankData;
    var testData = blankData;

    // ---Compute all statistics---
    var testAvg = 0;  // test average
    var hwAvg = 0;    // homework average

    // Calculate homework average
    for (var i = 0; i < document.getElementsByClassName
        ('form-control hw-input').length; i += 2) {
      hwValues.push((document.
        getElementsByClassName('form-control hw-input')[i].value) /
        (document.getElementsByClassName('form-control hw-input')[i + 1].
        value) * 100);
      hwAvg += Number(hwValues[i / 2]);
    }

    if (document.getElementsByClassName('form-control hw-input').length != 0) {
      hwAvg /= document.getElementsByClassName('form-control hw-input').
        length / 2;
    }

    // Calculate test Average
    for (var i = 0; i < document.
      getElementsByClassName('form-control test-input').length; i += 2) {
      testValues.push((document.
        getElementsByClassName('form-control test-input')[i].value) /
        (document.
        getElementsByClassName('form-control test-input')[i + 1].
        value) * 100);
      testAvg += Number(testValues[i / 2]);
    }

    if (document.getElementsByClassName('form-control test-input').
      length != 0) {
      testAvg /= document.getElementsByClassName('form-control test-input').
        length / 2;
    }

    // Update all statistics values on DOM
    document.getElementById('test-avg').value = (testAvg).toFixed(2);
    document.getElementById('hw-avg').value = (hwAvg).toFixed(2);

    // Calculate grade to date
    var gtd = 0;        // Overall grade to date

    if (document.getElementsByClassName('form-control test-input').
      length != 0 && document.
      getElementsByClassName('form-control hw-input').length != 0) {
      gtd += Number(document.getElementById('test-avg').value / 100) *
        Number(document.getElementById('test-weight').value);
      gtd += Number(document.getElementById('hw-avg').value / 100) *
        Number(document.getElementById('hw-weight').value);
    }

    // Update grade to date field
    document.getElementById('gtd').value = (gtd).toFixed(2);

    // Update the charts.
    hwChart.destroy();
    hwData = getChartData(hwValues);
    hwChart = new Chart(hwCtx).Line(hwData, options);
    testChart.destroy();
    testData = getChartData(testValues);
    testChart = new Chart(testCtx).Line(testData, options);

    /**
     * Generates an array of labels for a chart based on some provided data
     *
     * Grabs all hw and test items from the dom lists, then computes then
     * average for each and final grade based on the weights.
     * It then uses the values collected to generate new, updated charts.
     *
     * @param {Array} data - An Array of numbers.
     *
     * @return {Array} An array of labels (strings) that correspond to the data
     *     provided.
     */
    function getLabels(data) {
      var labels = [];
      for (var i = 1; i <= data.length; i++) {
        labels.push(i.toString());
      }
      return labels;
    }

    /**
     * Generates a Chart.js data object based on the given arrays.
     *
     * @param {Array} values - An Array of numbers.
     *
     * @return {Object} An object with two properties: labels and datasets.
     *     labels is an Array of strings and datasets is an Array of objects,
     *     each of which specifies the data and color of the chart.
     *     This object structure is required by Chart.js.
     */
    function getChartData(values) {
      var data = {
        labels: [],
        datasets: [
          {
            label: 'My First dataset',
            fillColor: 'rgba(220,220,220,0.2)',
            strokeColor: 'rgba(220,220,220,1)',
            pointColor: 'rgba(220,220,220,1)',
            pointStrokeColor: '#fff',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgba(220,220,220,1)',
            data: []
          },
        ]
      };

      // Populate the x axis of the graph
      data.labels = getLabels(values);

      // Populate data points
      for (var i = 0; i < values.length; i++) {
        data.datasets[0].data.push(values[i]);
      }

      return data;
    }
  }

  /**
   * Gets current test weight from the DOM, validates it, and updates
   * the statistics.
   *
   * @return {undefined} No return
   */
  function updatedTestWeight() {
    // Have to convert it to Number because everything from the DOM is a string
    var newtest = Number(document.getElementById('test-weight').value);

    // If we fail to convert, just set it to zero
    if (isNaN(newtest)) {
      newtest = 0;
    }
    // If the value is outside the appropriate range 0-100, don't allow it
    if (newtest < 0) {
      newtest = 0;
    } else if (newtest > 100) {
      newtest = 100;
    }

    // Update DOM elements
    document.getElementById('test-weight').value = newtest;

    document.getElementById('hw-weight').value = 100 - newtest;

    // Update statistics
    updateStats();

  }

  /**
   * Gets current HW weight from the DOM, validates it, and updates
   * the statistics.
   *
   * @return {undefined} No return
   */
  function updatedHwWeight() {
    // Have to convert it to Number because everything from the DOM is a string
    var newhw = Number(document.getElementById('hw-weight').value);

    // If we fail to convert, just set it to zero
    if (isNaN(newhw)) {
      newhw = 0;
    }

    // If the value is outside the appropriate range 0-100, don't allow it
    if (newhw < 0) {
      newhw = 0;
    } else if (newhw > 100) {
      newhw = 100;
    }

    // Update DOM elements
    document.getElementById('hw-weight').value = newhw;

    document.getElementById('test-weight').value = 100 - newhw;

    // Update statistics
    updateStats();

  }

  /**
   * Adds an input element to the DOM for the specified list type, 'pre'.
   *
   * Creates a uniquely identifiable list item and appends it to the
   * appropriate DOM list.  'Appropriate' is determined by the 'pre' variable
   * provided, which means the DOM lists must have ID's following the format:
   * '{pre}-list'.
   * Once the list item is added, the list item's 'on input' event is given a
   * handler, and its button given a delete click event.
   * Lastly, the 'no records' alert is is either hidden or shown and the
   * statistics are updated.
   *
   * @param {string} pre - A list designation: 'hw' or 'test'
   *
   * @return {undefined} No return
   */
  function add(pre) {
    // The counter is just a convenient globally unique identifier
    counter++;

    // Build template
    var id = `${pre}-${counter}`;
    var template = `
      <div id='${id}' class='list-group-item'>
        <div class='input-group'>
          <input id='${id}-num' class='form-control ${pre}-input' value='0' />
          <span class='input-group-addon'>/</span>
          <input id='${id}-den' class='form-control ${pre}-input' value='100' />
          <span class='input-group-btn'>
            <button id='${id}-delete' class='btn btn-danger' type='button'>
              <i class='fa fa-times'></i>
            </button>
          </span>
        </div>
      </div>
    `;

    // Add new element to DOM
    if (pre == 'hw') {
      document.getElementById('hw-list').
        insertAdjacentHTML('beforeend', template);
      hwCount++;

    } else {
      document.getElementById('test-list').
        insertAdjacentHTML('beforeend', template);
      testCount++;
    }

    // Validate and update all statistics when numerator input field changes
    document.getElementById(id + '-num').addEventListener('change', function() {
      if (document.getElementById(id + '-num').value < 0) {
        document.getElementById(id + '-num').value = 0;
      } else if (isNaN(Number(document.getElementById(id + '-num').value))) {
        console.log('yep');
        document.getElementById(id + '-num').value = 0;
      }

      // Get rid of leading zeros
      document.getElementById(id + '-num').value =
        document.getElementById(id + '-num').value.replace(/^[0]+/g,'');

      updateStats();
    });

    // Validate and update all statistics when denominator input field changes
    document.getElementById(id + '-den').addEventListener('change', function() {
      if (document.getElementById(id + '-den').value < 1 ||
        isNaN(document.getElementById(id + '-den').value)) {
        document.getElementById(id + '-den').value = 1;
      }

      // Get rid of leading zeros
      document.getElementById(id + '-den').value =
        document.getElementById(id + '-den').value.replace(/^[0]+/g,'');

      updateStats();
    });

    // Hook up delete button event
    document.getElementById(id + '-delete').
      addEventListener('click', function() {
      document.getElementById(id).remove();

      // Keep track of homework and test count for hiding
      if (pre == 'hw') {
        hwCount--;
      } else {
        testCount--;
      }

      hideNoRecords(pre);

      updateStats();
    });

    // Check if we can hide the 'no records' item
    hideNoRecords(pre);

    // Update the stats to reflect the addition
    updateStats();
  }

  function hideNoRecords(pre) {
    // Check if we can hide the 'no records' item
    if (pre == 'hw') {
      if (hwCount != 0) {
        document.getElementById('no-hw').style.display = 'none';
      } else {
        document.getElementById('no-hw').style.display = 'block';
      }
    } else {
      if (testCount != 0) {
        document.getElementById('no-test').style.display = 'none';
      } else {
        document.getElementById('no-test').style.display = 'block';
      }
    }
  }

})();
