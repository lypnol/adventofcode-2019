const _ = require("lodash/fp");

function required_fuel(mass) {
    return _.floor(mass/3) - 2;
}

const run = _.flow(
    _.split("\n"),
    _.map(_.parseInt(10)),
    _.map(required_fuel),
    _.sum,
);

console.log(run(process.argv[2]));
