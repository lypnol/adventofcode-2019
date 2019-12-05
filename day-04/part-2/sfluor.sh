#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1

function run() {
    # Your code goes here
    start=${INPUT:0:6}
    end=${INPUT:7:14}

    # Return answer
    seq $start $end |
        grep -P '([1-9])\1{1}' |
        grep -v '9[0-8]\|8[0-7]\|7[0-6]\|6[0-5]\|5[0-4]\|4[0-3]\|3[0-2]\|2[0-1]\|10' |
        # Remove 6 then, 5, 4, 3 consecutive same characters
        sed -r 's/([0-9])\1{5}//g' |
        sed -r 's/([0-9])\1{4}//g' |
        sed -r 's/([0-9])\1{3}//g' |
        sed -r 's/([0-9])\1{2}//g' |
        grep -P '([1-9])\1{1}' |
        wc -l
}

echo $(run)
