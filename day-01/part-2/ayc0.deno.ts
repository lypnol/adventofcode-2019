const fuelForMass = (mass: number) => {
  const massFuel = Math.floor(mass / 3) - 2;
  if (massFuel <= 0) {
    return 0;
  }
  return massFuel + fuelForMass(massFuel);
};

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s: string): unknown => {
  let sum = 0;
  s.split("\n").forEach(fuel => {
    sum += fuelForMass(parseInt(fuel));
  });
  return sum;
};

let start = Date.now();
let answer = run(Deno.args[1]);

console.log("_duration:" + (Date.now() - start).toString());
console.log(answer);
