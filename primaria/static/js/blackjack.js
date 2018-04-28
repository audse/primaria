var suits = ["clubs", "hearts", "spades", "diamonds"];
var suit_index;
var numbers = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"];
var number_index;
var i = 0;

var canvas_width = 600;
var canvas_height = 400;

var card_width = 75;
var card_height = 107;
var player_x = 100;
var player_y = 300;
var house_x = 500;
var house_y = 100;

var house_total;
var player_total;

var player_index = 0;
var house_index = 0;

var deck = [];
var player_hand = [];
var house_hand = [];
var back = new Image();

function Card(number, suit, image_src) {
  this.number = number;
  if (number > 10) {
    number = 10 // Face cards are 10 in blackjack
  }
  this.value = number;
  this.suit = suit;
  this.image = new Image();
  this.image.src = image_src;

  this.dealt = 0;
}

function build_deck() {
  for (suit_index=0; suit_index<4; suit_index++) {
    for (number_index=0; number_index<13; number_index++) {
      image_src = "{% static 'img/game/cards' %}" + numbers[number_index] + "_of_" + suits[suit_index] + ".png";
      deck[i] = new Card(number_index+1, suits[suit_index], image_src);
    }
  }
}

function deal_from_deck(who) {
  var card;

  var ch = 0;
  while ((deck[ch].dealt>0) && (ch<51)) {
    ch++
  }

  if (ch >= 51) {
    ctx.fillText("Deck finished.", 200, 200);
    ch = 51;
  }

  deck[ch].dealt = who;
  card = deck[ch];
  return card;
}

function start_deal() {
  player_hand[player_index] = deal_from_deck(1);
  ctx.drawImage(player_hand[player_index].image, player_x, player_y, card_width, card_height);
  player_x = player_x + 30;
  player_index++;

  house_hand[house_index] = deal_from_deck(2);
  ctx.drawImage(card_back, house_x, house_y, card_width, card_height)
  house_x = house_x + 20;
  house_index++;

  player_hand[player_index] = deal_from_deck(1);
  ctx.drawImage(player_hand[player_index].image, player_x, player_y, card_width, card_height);
  player_x = player_x + 30;
  player_index++;

  house_hand[house_index] = deal_from_deck(2);
  ctx.drawImage(house_hand[house_index], house_x, house_y, card_width, card_height)
  house_x = house_x + 20;
  house_index++;
}

function more_to_house() {
  var ace_count = 0;
  var i;
  var sum_up = 0;

  for (i=0; i<house_index; i++) {
    sum_up += house_hand[i].value;
    if (house_hand[i].value == 1) {
      ace_count++;
    }
  }

  if (ace_count > 0) {
    if ((sum_up+10) <= 21) {
      sum_up += 10;
    }
  }

  house_total = sum_up;
  if (sum_up < 17) {
    return true;
  } else {
    return false;
  }
}

function add_up_player() {
  var ace_count = 0;
  var i;

  var sum_up = 0;
  for (i=0; i<player_index; i++) {
    sum_up += player_hand[player_index].value;

    if (player_hand[player_index].value == 1) {
      ace_count++;
    }
  }
  if (ace_count > 0) {
    if ((sum_up + 10) <= 21) {
      sum_up += 10;
    }
  }
  return sum_up;
}

function player_done() {
  while(more_to_house()) {
    house_hand[house_index] = deal_from_deck(2);
    ctx.drawImage(back, house_x, house_y, card_width, card_height);
    house_x = house_x + 20;
    house_index ++;
  }

  show_house();
  player_total = add_up_player();
  if (player_total > 21) {
    if (house_total > 21) {
      ctx.fillText("You and house both went over.", 30, 100);
    } else {
      ctx.fillText("You went over and lost.", 30, 100);
    }
  } else if (house_total > 21) {
    ctx.fillText("You won. House went over.", 30, 100);
  } else if (player_total >= house_total) {
    if (player_total > house_total) {
      ctx.fillText("You won.", 30, 100);
    } else {
      ctx.fillText("You tied.", 30, 100);
    }
  } else if (house_total <= 21) {
      ctx.fillText("You lost.", 30, 100);
  } else {
    ctx.fillText("You won because house went over.", 30, 100);
  }
}

function new_game() {
  ctx.clearRect(0, 0, canvas_width, canvas_height);
  player_index = 0;
  house_index = 0;
  player_x = 100;
  house_x = 100;
  deal_start();
}

function show_house() {
  var i;
  house_x = 500;
  for (i=0; i<house_index; i++) {
    ctx.drawImage(house_hand[i].image_src, house_x, house_y, card_width, card_height);
    house_x = house_x + 20;
  }
}

function shuffle_deck() {
  var i = deck.length - 1;
  var s;
  while (i > 0) {
    s = Math.floor(Math.random()*(i+1));
    swap_in_deck(s, i);
    i--;
  }
}

function swap_in_deck(card_1, card_2) {
  var hold = new Card(deck[card_1].num, deck[card_1].suit, deck[card_1].picture.src);
  deck[card_1] = deck[card_2];
  deck[card_2] = hold;
}

function deal() {
  player_hand[player_index] = deal_from_deck(1);
  ctx.drawImage(player_hand[player_index].image, player_x, player_y, card_width, card_height);
  player_x = player_x + 30;
  player_index++;

  if (more_to_house()) {
    house_hand[house_index] = deal_from_deck(2);
    ctx.drawImage(house_hand[house_index], house_x, house_y, card_width, card_height)
    house_x = house_x + 20;
    house_index++;
  }
}

function init() {
  ctx = document.getElementById('blackjack').getContext('2d');
  ctx.font = "italic 20pt Georgia";
  ctx.fillStyle = "green";

  build_deck();
  back.src = "red_joker.png";

  canvas_1 = document.getElementById("blackjack");
  window.addEventListener('keydown', 'getkey', false);
  shuffle_deck();
  start_deal();
}

function getkey(event) {
  var key_code;

  if (event == null) {
    key_code = window.event.keyCode;
    window.event.preventDefault();
  } else {
    key_code = event.keyCode;
    event.preventDefault();
  }

  switch(key_code) {
    case 68: // D
      deal();
      break;
    case 72: // H
      player_done();
      break;
    case 78: // N
      new_game();
      break;
    default:
      alert("Press D, H, or N")
  }
}
