class Solution {

    // This is your puzzle input
    private readonly input: string;

    constructor(input: string) {
        this.input = input;
    }

    run(): number {
        return this.input.split("\n")
            .map(v => Math.floor(parseInt(v) / 3) - 2)
            .reduce((acc, value) => acc + value, 0);
    }

    main() {
        const start = Date.now();
        const answer = this.run();

        console.log("_duration:" + (Date.now() - start).toString());
        console.log(answer);
    }
}

// @ts-ignore
const solution = new Solution(process.argv[2]);
solution.main();
