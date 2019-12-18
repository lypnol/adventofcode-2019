const fuelForMass = (fuel: number) => {
  return Math.floor(fuel / 3) - 2;
};

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
