'use strict';

let assert = require('assert');
let purchases = require('../purchases');

describe('purchases', function() {
  describe('filterPurchases()', function() {
    it('returns a new array of elements with a specified property of a ' +
       'specified value', function() {
      let input = [
        {name: 'bob', age: 45, height: '5.7'},
        {name: 'terry', age: 33, height: 5.5},
        {name: 'alice', age: 28, height: 5.7},
        {name: 'alice', age: 37, height: 5.2}
      ];
      let alices = purchases.filterPurchases(input, 'name', 'alice');
      assert.strictEqual(input.length, 4); // Don't modify original array
      // Make sure what we got back is actually correct.
      assert.strictEqual(alices.length, 2);
      assert.strictEqual(alices[0].name, 'alice');
      assert.strictEqual(alices[0].age, 28);
      assert.strictEqual(alices[0].height, 5.7);
      assert.strictEqual(alices[1].name, 'alice');
      assert.strictEqual(alices[1].age, 37);
      assert.strictEqual(alices[1].height, 5.2);
      // Make sure strict equality is used
      let height57 = purchases.filterPurchases(input, 'height', 5.7);
      assert.strictEqual(height57.length, 1);
      assert.strictEqual(alices[0].name, 'alice');
      assert.strictEqual(alices[0].age, 28);
      assert.strictEqual(alices[0].height, 5.7);
    });
  });
  describe('parsePurchaseCSV()', function() {
    it('converts a CSV string into to a list of objects', function() {
      let data = 'shoes, 2015-02-31, 49.99, TOPS\n' +
          'shirt, 2015-01-22, 15.50, REK\n' +
          'pants, 2014-12-05, 30.50, YA!';
      let parsedData = purchases.parsePurchaseCSV(data);
      let propertyList = ['item', 'date', 'price', 'store'];
      assert.strictEqual(parsedData.length, 3);
      for (let d of parsedData) {
        for (let p of propertyList) {
          assert.strictEqual(p in d, true);
        }
        assert.strictEqual(typeof(d.item), typeof(''));
        assert.strictEqual(typeof(d.date), typeof(new Date()));
        assert.strictEqual(typeof(d.price), typeof(5.5));
        assert.strictEqual(typeof(d.store), typeof(''));
      }
      // Note that this test does not fully verify proper setting of values.
    });
  });
  describe('countsByMonth()', function() {
    it('takes an array of objects and counts the number of occurrences, ' +
       'grouping by month and sorted by month ascending', function() {
      let data = [
        {date: new Date('2016-01-15')},
        {date: new Date('2016-02-16')},
        {date: new Date('2016-02-17')},
        {date: new Date('2016-03-18')},
        {date: new Date('2016-03-19')},
        {date: new Date('2016-03-20')},
        {date: new Date('2016-03-21')},
        {date: new Date('2015-12-22')},
        {date: new Date('2015-02-23')}
      ];
      let countsByMonth = purchases.countsByMonth(data);
      assert.strictEqual(countsByMonth.length, 12);
      assert.strictEqual(countsByMonth[0], 1);
      assert.strictEqual(countsByMonth[1], 3);
      assert.strictEqual(countsByMonth[2], 4);
      assert.strictEqual(countsByMonth[3], 0);
      assert.strictEqual(countsByMonth[4], 0);
      assert.strictEqual(countsByMonth[5], 0);
      assert.strictEqual(countsByMonth[6], 0);
      assert.strictEqual(countsByMonth[7], 0);
      assert.strictEqual(countsByMonth[8], 0);
      assert.strictEqual(countsByMonth[9], 0);
      assert.strictEqual(countsByMonth[10], 0);
      assert.strictEqual(countsByMonth[11], 1);
    });
  });
  describe('totalSpentByMonth()', function() {
    it('takes an array of objects and counts the amount spent, grouping by ' +
       'month and sorted by month ascending', function() {
      let data = [
        {date: new Date('2016-12-15'), price: 75.1},
        {date: new Date('2016-12-16'), price: 75.9},
        {date: new Date('2016-01-17'), price: 50},
        {date: new Date('2016-07-18'), price: 25.5},
        {date: new Date('2016-07-19'), price: 40},
        {date: new Date('2016-07-20'), price: 10},
        {date: new Date('2016-08-21'), price: 66},
        {date: new Date('2016-08-21'), price: 22},
        {date: new Date('2015-09-22'), price: 27},
        {date: new Date('2015-12-23'), price: 24}
      ];
      let spentByMonth = purchases.totalSpentByMonth(data);
      assert.strictEqual(spentByMonth.length, 12);
      assert.strictEqual(spentByMonth[0], 50);
      assert.strictEqual(spentByMonth[1], 0);
      assert.strictEqual(spentByMonth[2], 0);
      assert.strictEqual(spentByMonth[3], 0);
      assert.strictEqual(spentByMonth[4], 0);
      assert.strictEqual(spentByMonth[5], 0);
      assert.strictEqual(spentByMonth[6], 75.5);
      assert.strictEqual(spentByMonth[7], 88);
      assert.strictEqual(spentByMonth[8], 27);
      assert.strictEqual(spentByMonth[9], 0);
      assert.strictEqual(spentByMonth[10], 0);
      assert.strictEqual(spentByMonth[11], 175);
    });
  });
});
