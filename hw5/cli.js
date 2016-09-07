/**
 * CLI Parsing Utilities
 *
 * @module cli
 */
'use strict';

// Third party CLI argument parsing library, installed with NPM
let argparse = require('argparse');

/**
 * Parses command line arguments.
 *
 * Parses command line arguments and returns the parsed values. If the
 * values were bad (missing required args, bad args, etc), the program
 * will be killed.
 *
 * The returned `Namespace` object has the following properties:
 *
 * - `item` (*string*): The name of an item to filter on. `null` if
 *   no item was supplied.
 *
 * - `store` (*string*): The name of an store to filter on. `null` if
 *   no store was supplied.
 *
 * - `total` (*boolean*): `true` if the user wants the chart to reflect
 *   the total dollar amount spent, otherwise `false`.
 *
 * - `scale` (*int*): The scale to use for the Y-axis in printed charts.
 *
 * @return {Object} a Namespace object
 */
module.exports.parseArgs = function() {
  // Create a new argument parser
  let parser = new argparse.ArgumentParser({
    version: '1.0.0',
    addHelp: true,
    description: 'Purchase history plotter'
  });

  parser.addArgument(
    ['--store'],
    {
      help: 'Show purchase history for this store.'
    }
  );

  parser.addArgument(
    ['--item'],
    {
      help: 'Show purchase history for this item.'
    }
  );

  parser.addArgument(
    ['--total'],
    {
      action: 'storeTrue',
      help: 'Plot by total dollar amount instead of purchase count.'
    }
  );

  parser.addArgument(
    ['--scale'],
    {
      type: 'int',
      help: 'Scale the Y-axis by counting by this value (instead of by 1\'s).'
    }
  );

  return parser.parseArgs();
};
