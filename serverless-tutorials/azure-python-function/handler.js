'use strict';
import { Series, DataFrame } from 'pandas-js';

/* eslint-disable no-param-reassign */

module.exports.hello = function (context) {
  const ds = new Series([1, 2, 3, 4], {name: 'My test name', index: [2, 3, 4, 5]})
  const dsString = ds.toString()

  context.log('JavaScript HTTP trigger function processed a request.');

  context.res = {
    // status: 200, /* Defaults to 200 */
    body: dsString
  };

  context.done();
};
