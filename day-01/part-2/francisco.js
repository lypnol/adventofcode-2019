const _ = require("lodash/fp");

function required_fuel(mass) {
    return _.floor(mass/3) - 2;
}

function required_fuel_2(mass) {
    const requirement = required_fuel(mass);
    return requirement < 0 ? 0 : requirement + required_fuel_2(requirement);
}

const run = _.flow(
    _.split("\n"),
    _.map(_.parseInt(10)),
    _.map(required_fuel_2),
    _.sum,
);

console.log(run(process.argv[2]));
