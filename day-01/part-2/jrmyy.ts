class Solution {

	// This is your puzzle input
	private readonly input: string;

	constructor(input: string) {
		this.input = input;
	}

	getFuel(value: number, fuelSum = 0): number {
		const fuelRes = Math.floor(value / 3) - 2;
		return fuelRes < 0 ? fuelSum : this.getFuel(fuelRes, fuelSum + fuelRes);
	}

	run(): number {
		return this.input.split('\n')
			.map(v => this.getFuel(parseInt(v, 10)))
			.reduce((acc, value) => acc + value, 0);
	}

	main() {
		const start = Date.now();
		const answer = this.run();

		console.log(`_duration:${(Date.now() - start).toString()}`);
		console.log(answer);
	}
}

// @ts-ignore
const solution = new Solution(process.argv[2]);
solution.main();
