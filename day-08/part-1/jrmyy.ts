import * as _ from 'lodash';

class Solution {

    // This is your puzzle input
    private readonly input: string;

    constructor(input: string) {
        this.input = input;
    }

    run(): number {
        const ints = this.input.split('').map(v => Number(v));
        const layerSize = 25 * 6;
        const layers = _.chunk(ints, layerSize).map(layer => _.countBy(layer));
        const rightLayer = layers.sort((a, b) => a['0'] - b['0'])[0];
        return rightLayer['1'] * rightLayer['2'];
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
