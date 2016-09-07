'use strict';

let cli = require('./cli');
let printer = require('./printer');
let purchases = require('./purchases');

// Parse CLI Args
let args = cli.parseArgs();

// Initialize our file data to the empty string
let fileData = '';

// Set the encoding for stdin to "ascii", so that the data we read in
// will already be encoded as ASCII.
process.stdin.setEncoding('ascii');

// process.stdin is a stream.Readable. Readables emit certain events
// that we can subscribe to. In this case, whenever the process.stdin
// object pulls data off of standard input, our anonymous function
// will be called.
process.stdin.on('data', function(dataChunk) {
  // Whenever process.stdin has new data to give us, we add it to the
  // string that we've been accumulating.
  fileData += dataChunk;
});

// As a stream.Readable, process.stdin also emits an 'end' event,
// which fires when there's absolutely nothing left to read at the end
// of the file (i.e., it reaches EOF). When that happens, then we know
// that we're done reading data from standard input, so we can process
// our complete data file, which has been accumulated in fileData.
process.stdin.on('end', function() {
  // Parse and load data from the CSV data that we've read in
  let csvData = purchases.parsePurchaseCSV(fileData);

  // Names for the sake of output
  let item = 'all item';
  let store = 'all stores';

  // User specified an item to filter on
  if (args.item !== null) {
    item = args.item;
    csvData = purchases.filterPurchases(csvData, 'item', args.item);
  }

  // User specified a store to filter on
  if (args.store !== null) {
    store = args.store;
    csvData = purchases.filterPurchases(csvData, 'store', args.store);
  }

  // Condense data into chart-ready form
  let condensed;
  if (args.total) {
    // Stores dollar amounts if we're using totals
    condensed = purchases.totalSpentByMonth(csvData);
  } else {
    // Stores count if we're not using totals
    condensed = purchases.countsByMonth(csvData);
  }

  // If the user specified a scale, we'll use that.
  let scale = 1;
  if (args.scale !== null) {
    scale = args.scale;
  }

  // Output a generic title for the chart
  console.log('Purchase history for ' + item + 's at ' + store + '.');

  // Output the chart
  console.log(printer.toChart(condensed, scale));
});
