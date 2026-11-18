
/* 1. MANY WORLDS */

const worlds = {
  games: {
    label: "GAMING",
    image: "images/gaming.jpg",
    alt: "Astronaut playing an arcade game",
    title: "Play to explore",
    text: "In games, play is a way to test ideas, solve problems and experience imaginary worlds."
  },
  music: {
    label: "MUSIC",
    image: "images/music.jpg",
    alt: "Astronaut playing an electric guitar",
    title: "Play to express",
    text: "We play instruments, rhythms and songs. Here, play turns feeling into sound."
  },
  sports: {
    label: "SPORTS",
    image: "images/sport.jpg",
    alt: "Astronaut playing basketball in space",
    title: "Play to connect",
    text: "A match creates teamwork, movement, friendly competition and shared rules."
  },
  theatre: {
    label: "THEATRE",
    image: "images/theatre.jpg",
    alt: "Astronaut dressed as a wizard holding a magic staff",
    title: "Play a different role",
    text: "A play is a story on stage. To play a character is to step into someone else's world."
  },
  technology: {
    label: "TECHNOLOGY",
    image: "images/tehnology.jpg",
    alt: "Astronaut using a smartphone",
    title: "Press play",
    text: "One small triangle can start a video, a song or an entirely new experience."
  }
};

// Update the selected world
const worldButtons = document.querySelectorAll(".world-btn");

function showWorld(name) {
  const world = worlds[name];
  if (!world) return;

  const image = document.querySelector("#worldGraphic");
  image.src = world.image;
  image.alt = world.alt;

  document.querySelector("#worldLabel").textContent = world.label;
  document.querySelector("#worldTitle").textContent = world.title;
  document.querySelector("#worldText").textContent = world.text;

  worldButtons.forEach(button => {
    const active = button.dataset.world === name;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

worldButtons.forEach(button => {
  button.addEventListener("click", () => showWorld(button.dataset.world));
});

showWorld("games");


/* 2. MUSIC VIBE QUIZ */

const musicQuestions = [
  {
    question: "What makes you press play?",
    answers: [
      ["A beat that gets me moving", "energetic"],
      ["A melody that matches my mood", "dreamer"],
      ["Something new and unexpected", "explorer"]
    ]
  },
  {
    question: "Where do you enjoy music most?",
    answers: [
      ["At a concert or party", "energetic"],
      ["Alone with my headphones", "dreamer"],
      ["Wherever I can discover new sounds", "explorer"]
    ]
  },
  {
    question: "What matters most in a song?",
    answers: [
      ["Rhythm and energy", "energetic"],
      ["Lyrics and emotion", "dreamer"],
      ["Creativity and originality", "explorer"]
    ]
  },
  {
    question: "Your perfect playlist is...",
    answers: [
      ["Full of upbeat anthems", "energetic"],
      ["A soundtrack to my feelings", "dreamer"],
      ["A mix of unexpected genres", "explorer"]
    ]
  }
];

const musicResults = {
  energetic: {
    emoji: "⚡",
    title: "The Energy Seeker",
    text: "You love rhythms that make you move. For you, pressing play means energy, excitement and fun!"
  },
  dreamer: {
    emoji: "🌙",
    title: "The Dreamy Listener",
    text: "Music is your personal soundtrack. You connect with melodies, memories and meaningful lyrics."
  },
  explorer: {
    emoji: "✨",
    title: "The Sound Explorer",
    text: "You enjoy unexpected sounds and fresh artists. For you, play means discovery and creativity."
  }
};

let musicAnswers = [];
let musicStep = 0;

// Determine the most common answer category
function calculateMusicResult() {
  const scores = { energetic: 0, dreamer: 0, explorer: 0 };
  musicAnswers.forEach(answer => scores[answer]++);

  // If scores are tied, prefer the first selected category
  return musicAnswers.reduce(
    (best, answer) => scores[answer] > scores[best] ? answer : best,
    musicAnswers[0]
  );
}

// Show the current question or the final result
function renderMusicQuiz() {
  const total = musicQuestions.length;
  const complete = musicStep === total;
  const progress = Math.round(musicStep / total * 100);

  document.querySelector("#quizQuestionArea").hidden = complete;
  document.querySelector("#quizResult").hidden = !complete;
  document.querySelector("#quizProgress").setAttribute("aria-valuenow", musicStep);
  document.querySelector("#quizProgressFill").style.width = `${progress}%`;
  document.querySelector("#quizPercent").textContent = `${progress}%`;

  if (complete) {
    const result = musicResults[calculateMusicResult()];
    document.querySelector("#quizStep").textContent = "QUIZ COMPLETE";
    document.querySelector("#quizResultEmoji").textContent = result.emoji;
    document.querySelector("#quizResultTitle").textContent = result.title;
    document.querySelector("#quizResultText").textContent = result.text;
    return;
  }

  const current = musicQuestions[musicStep];
  const options = document.querySelector("#quizOptions");

  document.querySelector("#quizStep").textContent =
    `QUESTION ${musicStep + 1} OF ${total}`;
  document.querySelector("#quizQuestion").textContent = current.question;
  document.querySelector("#quizBack").hidden = musicStep === 0;

  options.replaceChildren();

  current.answers.forEach(([answer, type], index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "quiz-option";
    button.textContent = `${String.fromCharCode(65 + index)}. ${answer}`;

    button.addEventListener("click", () => {
      musicAnswers[musicStep] = type;
      musicStep++;
      renderMusicQuiz();
    });

    options.append(button);
  });
}

// Navigate back or restart
document.querySelector("#quizBack").addEventListener("click", () => {
  if (musicStep > 0) {
    musicStep--;
    musicAnswers.pop();
    renderMusicQuiz();
  }
});

document.querySelector("#quizRestart").addEventListener("click", () => {
  musicAnswers = [];
  musicStep = 0;
  renderMusicQuiz();
});

renderMusicQuiz();


/* 3. ROCK PAPER SCISSORS */

const rpsChoices = { rock: "✊", paper: "✋", scissors: "✌️" };
let playerScore = 0;
let computerScore = 0;

function playRPS(player) {
  const choices = Object.keys(rpsChoices);
  const computer = choices[Math.floor(Math.random() * choices.length)];

  document.querySelector("#playerChoice").textContent = rpsChoices[player];
  document.querySelector("#computerChoice").textContent = rpsChoices[computer];

  let message;

  if (player === computer) {
    message = "It's a tie! 🤝";
  } else if (
    (player === "rock" && computer === "scissors") ||
    (player === "paper" && computer === "rock") ||
    (player === "scissors" && computer === "paper")
  ) {
    playerScore++;
    message = "You win!";
  } else {
    computerScore++;
    message = "Computer wins! Try again!";
  }

  document.querySelector("#playerScore").textContent = playerScore;
  document.querySelector("#computerScore").textContent = computerScore;
  document.querySelector("#rpsMessage").textContent = message;
}

document.querySelectorAll(".rps-btn").forEach(button => {
  button.addEventListener("click", () => playRPS(button.dataset.choice));
});

document.querySelector("#rpsReset").addEventListener("click", () => {
  playerScore = 0;
  computerScore = 0;

  document.querySelector("#playerScore").textContent = "0";
  document.querySelector("#computerScore").textContent = "0";
  document.querySelector("#playerChoice").textContent = "❔";
  document.querySelector("#computerChoice").textContent = "❔";
  document.querySelector("#rpsMessage").textContent = "Choose your move to start!";
});


/* 4. HIGHER OR LOWER */

const suits = ["♠", "♥", "♦", "♣"];
const cardNames = { 1: "A", 11: "J", 12: "Q", 13: "K" };

let hlDeck = [];
let hlCurrent = null;
let hlScore = 0;
let hlBest = 0;

// Shuffle cards using Fisher-Yates
function shuffled(items) {
  const result = [...items];

  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }

  return result;
}

// Create a standard deck of 52 cards
function makeDeck() {
  const deck = [];

  suits.forEach(suit => {
    for (let value = 1; value <= 13; value++) {
      deck.push({ value, suit });
    }
  });

  return shuffled(deck);
}

function cardLabel(card) {
  return (cardNames[card.value] || card.value) + card.suit;
}

// Draw a card; create a new deck when the current one is empty
function drawCard() {
  if (hlDeck.length === 0) hlDeck = makeDeck();
  return hlDeck.pop();
}

// Update the displayed card
function showCurrentCard() {
  const element = document.querySelector("#hlCard");
  element.replaceChildren();

  element.append(document.createTextNode(cardNames[hlCurrent.value] || hlCurrent.value));

  const suit = document.createElement("span");
  suit.textContent = hlCurrent.suit;
  element.append(suit);

  element.classList.toggle("red-suit", ["♥", "♦"].includes(hlCurrent.suit));
  element.setAttribute("aria-label", "Current card: " + cardLabel(hlCurrent));
}

function startHigherLower() {
  hlDeck = makeDeck();
  hlCurrent = drawCard();
  hlScore = 0;

  document.querySelector("#hlScore").textContent = "0";
  document.querySelector("#hlBest").textContent = hlBest;
  document.querySelector("#hlNext").textContent = "?";
  document.querySelector("#hlMessage").textContent = "Will the next card be higher or lower?";

  showCurrentCard();
}

// Compare the next card with the current one
function guessHigherLower(direction) {
  const next = drawCard();
  const tie = next.value === hlCurrent.value;
  const correct = direction === "higher"
    ? next.value > hlCurrent.value
    : next.value < hlCurrent.value;

  if (correct) {
    hlScore++;
    hlBest = Math.max(hlBest, hlScore);
  } else {
    hlScore = 0;
  }

  document.querySelector("#hlScore").textContent = hlScore;
  document.querySelector("#hlBest").textContent = hlBest;

  let message;
  if (tie) {
    message = `It was a tie (${cardLabel(next)}). Streak reset!`;
  } else if (correct) {
    message = `Correct! Next card was ${cardLabel(next)}.`;
  } else {
    message = `Not quite! It was ${cardLabel(next)}. Try again!`;
  }

  document.querySelector("#hlMessage").textContent = message;
  hlCurrent = next;
  showCurrentCard();
}

document.querySelector("#higherBtn").addEventListener("click", () => guessHigherLower("higher"));
document.querySelector("#lowerBtn").addEventListener("click", () => guessHigherLower("lower"));
document.querySelector("#hlReset").addEventListener("click", startHigherLower);

startHigherLower();
