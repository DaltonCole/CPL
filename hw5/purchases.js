/**
 * Purchase parsing and manipulation utilities
 *
 * The functions in this module are intended to help work with CSV
 * data acquired from a data file.
 *
 * Rows of CSV must be formatted with the following columns:
 *
 * 1. The type of the item (coat, hat, etc.)
 * 2. The date formatted in **ISO 8601** string format
 * 3. The price of the item
 * 4. The name of the store
 *
 * Objects can be loaded from this type of data. They have the
 * following properties:
 *
 * - `item` - A `string`
 * - `date` - A [`Date` object](https://goo.gl/Moqb2z)
 * - `price` - A `number`
 * - `store` - A `string`
 *
 * @example
 * { item: 'gloves',
 *   date: Fri Dec 25 2015 14:54:00 GMT-0600 (CST), // a Date object
 *   price: 44.65, // a number primitive
 *   store: 'OKNY' }
 *
 * @module purchases
 */
'use strict';

/**
 * Filters a list of purchases based on an expected field.
 *
 * @example
 * // returns an Array of the objects from myArray whose price
 * // property is strictly equal to 10.00
 * filterPurchases(myArray, "price", 10.00);
 *
 * @param {Array} purchases - An Array of purchase objects
 * @param {string} field - The name of the field to filter on *
 * @param {any} value - The value to compare against
 *
 * @returns {Array} - Returns an Array of items, where every item's
 *     `field` property is equal to `value`
 */
module.exports.filterPurchases = function(purchases, field, value) {
  // Create an empty list
  let filtered = [];
  // For each purchased item:
  for (let i = 0; i < purchases.length; i++) {
    // If the purchased item is the same as value, add it to the list
    if (purchases[i][field] === value) {
      filtered.push(purchases[i]);
    }
  }

  return filtered;
};

/**
 * Parses purchase information from a string of CSV data.
 *
 * Lines of CSV must be formatted with the following columns:
 *
 * 1. The type of the item (coat, hat, etc.)
 * 2. The date formatted in ISO 8601 string format
 * 3. The price of the item
 * 4. The name of the store
 *
 * @param {string} csvData - A multi-line string of CSV data
 *
 * @return {Array} - An Array of loaded purchases, as described above.
 */
module.exports.parsePurchaseCSV = function(csvData) {
  // Split the csv file by lines
  let lines = csvData.split(/\r?\n/);
  // Create an empty list to split a single line on
  let sLine = [];
  // Empty list for the parsed purchases
  let parsed = [];
  for (let i of lines) {
    // Split each line into four elements
    sLine = i.split(',');
    // Makes an object with four elements
    sLine = {item: sLine[0], date: sLine[1], price: sLine[2], store: sLine[3]};
    // Change string to type Date
    sLine.date = new Date(sLine.date);
    // Change string to type Number
    sLine.price = Number(sLine.price);
    // Add newly created object to the end of parsed list
    parsed.push(sLine);
  }

  return parsed;
};

/**
 * Count the number of purchases made per month.
 *
 * **Note**: this function assumes that all purchase dates occur
 * within the same calendar year.
 *
 * @param {Array} purchases - The array of purchase objects
 *
 * @return {Array} - An Array of 12 numbers -- indicating the number
 *     of purchases made in January (index 0) through December (index
 *     11). The numbers will be integers.
 */
module.exports.countsByMonth = function(purchases) {
  // Initialize a list with 12 zeroed elements
  let months = [0,0,0,0,0,0,0,0,0,0,0,0];

  // For each element in purchases
  for (let i = 0; i < purchases.length; i++) {
    // Add one to the month an item was purchased
    months[purchases[i].date.getMonth()]++;
  }

  return months;
};

/**
 * Sum the total amount of money spent per month.
 *
 * **Note**: this function assumes that all purchase dates occur
 * within the same calendar year.
 *
 * @param {Array} purchases - The array of purchase objects
 *
 * @return {Array} - An Array of 12 numbers -- indicating the amount
 *     of money spent during January (index 0) through December (index
 *     11). The numbers may be floating point.
 */
module.exports.totalSpentByMonth = function(purchases) {
  // Initialize a list with 12 zeroed elements
  let spent = [0,0,0,0,0,0,0,0,0,0,0,0];

  // For each element in purchases
  for (let i = 0; i < purchases.length; i++) {
    // Add the price of the item to the month it was purchased
    spent[purchases[i].date.getMonth()] += purchases[i].price;
  }

  return spent;
};
