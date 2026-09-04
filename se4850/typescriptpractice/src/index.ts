// arrays
function add(...numbers: number[]): number {
  return numbers.reduce((acc, curr) => acc + curr, 0);
}

let scores: number[] = [85,42,111];
let animals: string[] = ["cat", "dog", "spidermonkey"];
let scores3: Array<number> = [1,2,3];
let active: boolean[] = [true, true, false];

scores.push(100);
// console.log(add(...scores));
console.log("UPDATED");

for (let i = 0; i < animals.length; i++) {
  console.log(animals[i]);
}

// map -> changing everything
let doubled:number[] = [];
for (let number of scores) {
    doubled.push(number * 2);
}
// OR
let mappedDouble:number[] = scores.map((num) => num * 2);
let mappedAnnounce:string[] = animals.map((str) => str + " is a great animal");

console.log(mappedDouble);
console.log(mappedAnnounce);

// 9/4/class
interface Test {
  name: string;
  grade: number;
  active?: boolean; // optional property = Undefined
}

const student: Test = {
  name: "bob",
  grade: 90,
}

console.log(student.name);
console.log(student.grade);
console.log(student.active);
