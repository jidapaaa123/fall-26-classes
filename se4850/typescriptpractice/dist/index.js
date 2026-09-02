"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// arrays
function add(...numbers) {
    return numbers.reduce((acc, curr) => acc + curr, 0);
}
let scores = [85, 42, 111];
let animals = ["cat", "dog", "spidermonkey"];
let scores3 = [1, 2, 3];
let active = [true, true, false];
scores.push(100);
// console.log(add(...scores));
console.log("UPDATED");
for (let i = 0; i < animals.length; i++) {
    console.log(animals[i]);
}
// map -> changing everything
let doubled = [];
for (let number of scores) {
    doubled.push(number * 2);
}
// OR
let mappedDouble = scores.map((num) => num * 2);
let mappedAnnounce = animals.map((str) => str + " is a great animal");
console.log(mappedDouble);
console.log(mappedAnnounce);
//# sourceMappingURL=index.js.map