'use strict';

let assert = require('assert');
let printer = require('../printer');

describe('printer', function() {
  describe('toChart()', function() {
    it('returns only the X-axis if everything is zero', function() {
      assert.strictEqual(printer.toChart([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                   '   -J--F--M--A--M--J--J--A--S--O--N--D-');
    });

    it('puts an asterisk over the right month', function() {

      let chart;
      let expected;
      let xaxis = '   -J--F--M--A--M--J--J--A--S--O--N--D-';

      // January
      chart = printer.toChart([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
      expected = '1   *                                  \n' + xaxis;
      assert.strictEqual(expected, chart);

      // February
      chart = printer.toChart([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
      expected = '1      *                               \n' + xaxis;
      assert.strictEqual(expected, chart);

      // March
      chart = printer.toChart([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
      expected = '1         *                            \n' + xaxis;
      assert.strictEqual(expected, chart);

      // April
      chart = printer.toChart([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]);
      expected = '1            *                         \n' + xaxis;
      assert.strictEqual(expected, chart);

      // November
      chart = printer.toChart([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]);
      expected = '1                                 *    \n' + xaxis;
      assert.strictEqual(expected, chart);

      // December
      chart = printer.toChart([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]);
      expected = '1                                    * \n' + xaxis;
      assert.strictEqual(expected, chart);
    });

    it('scales appropriately', function() {
      let data = [0, 0, 0, 5, 0, 0, 0, 40, 25, 10, 50, 10];
      let chart = printer.toChart(data, 5);
      let expected = '';
      expected += '50                                 *    \n';
      expected += '45                                 *    \n';
      expected += '40                        *        *    \n';
      expected += '35                        *        *    \n';
      expected += '30                        *        *    \n';
      expected += '25                        *  *     *    \n';
      expected += '20                        *  *     *    \n';
      expected += '15                        *  *     *    \n';
      expected += '10                        *  *  *  *  * \n';
      expected += ' 5            *           *  *  *  *  * \n';
      expected += '    -J--F--M--A--M--J--J--A--S--O--N--D-';
      assert.strictEqual(expected, chart);

      chart = printer.toChart(data, 10);
      expected =  '50                                 *    \n';
      expected += '40                        *        *    \n';
      expected += '30                        *        *    \n';
      expected += '20                        *  *     *    \n';
      expected += '10                        *  *  *  *  * \n';
      expected += '    -J--F--M--A--M--J--J--A--S--O--N--D-';
      assert.strictEqual(expected, chart);
    });
  });
});
