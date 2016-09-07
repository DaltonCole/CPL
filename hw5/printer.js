/**
 * Chart Printing Utilities
 *
 * @module printer
 */
'use strict';

/**
 * Determines the height of the tallest column in an Array of column
 * heights.
 *
 * Given an array of values corresponding to the height of chart
 * columns, returns the height of the tallest column. In other words,
 * this is a max function for an Array of non-negative integers.
 *
 * @param {Array} columns - An Array of non-negative numbers.
 *
 * @returns {number} The height of the tallest column. If the height
 *     is a floating point value, it is rounded up to the next integer
 *     (via Math.ceil).
 */
function maxHeight(columns) {
  // Set initial max to 0
  let max = 0;

  // For each column
  for (let i = 0; i < columns.length; i++) {
    // If current column is larger than all previous columns
    if (max < columns[i]) {
      // Set max equal to the new column;
      max = columns[i];
    }
  }
  // Round max up if it is a floating point number
  max = Math.ceil(max);

  return max;
}

/**
 * Constructs an ASCII chart using an Array of values.
 *
 * Constructs an ASCII chart using an Array of twelve numeric values.
 * It is assumed that each index of the input Array corresponds with a
 * month of the year, starting with January. Index 0 is January, index
 * 1 is February, etc.
 *
 * Each value in the input Array corresponds to the height of the
 * corresponding month's column. If, for example, the first item in
 * the Array was a 5 (and `scale` was not provided), then the height
 * of the column for January would be 5.
 *
 * The height can be scaled using the `scale` parameter. The values on
 * the Y-axis will count by `scale`. For example, if the first item in
 * the array was 12, and the scale was 5, then the column would be
 * two `*`s high, and the Y-axis would count by fives.
 *
 * @param {Array} columns - An Array of values to print as a
 *     chart. Must be length 12. This parameter is required.
 *
 * @param {number} scale - An integer value to use as the scale for
 *     the chart's Y-axis. For example, a scale of 10 would set the
 *     Y-axis to count `10, 20, 30, ...`. If this parameter is not
 *     provided, a scale of 1 will be used.
 *
 * @return {string} The chart as a string: ready for printing.
 */
module.exports.toChart = function(columns, scale) {
  // Find the max height of the columns
  let mHeight = maxHeight(columns);
  // Initialize output to empty string
  let output = '';
  // If scale is not given, default it to zero
  if (scale === undefined) {
    scale = 1;
  }

  // Find the max number of spaces the y-axis will take up
  let spaceLength = String(mHeight).length;
  // Set the y-axis scale correctly
  for (let i = Math.floor(mHeight / scale); i > 0; i--) {
    // Find the number of spaces to put before a number in the y-axis
    for (let j = String(i * scale).length; j < spaceLength; j++) {
      output += ' ';
    }
    // y-axis label
    output += i * scale + ' ';
    // for each column, do the following
    for (let j of columns) {
      // Output two spaces to meet standard
      output += '  ';
      // If column has enough elements for the current row,
      // add star, if not, add space
      if (j / scale >= i) {
        output += '*';
      } else {
        output += ' ';
      }
    }
    // Start on new row
    output += ' \n';
  }
  // Standardize x-axis based on mHeight * scale
  for (let j = 1; j < spaceLength; j++) {
    output += ' ';
  }
  // Add x-axix
  output += '   -J--F--M--A--M--J--J--A--S--O--N--D-';

  return output;
};
