// assume that option 2 is the correct answer
const correctAnswer = "Button 4";
const buttons = document.querySelectorAll("button");
buttons.forEach(function(button) {
    button.addEventListener("click", function() {
        if (this.textContent === correctAnswer) {
            alert("Correct!");
            // code to store number of correct answers
        } else {
            alert("Incorrect!");
            // code to store number of incorrect answers
        }
    });
});
