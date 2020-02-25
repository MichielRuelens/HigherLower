import React from 'react';
import ReactDOM from 'react-dom';
import styles from './game.module.scss';
import CARD_BACK from "../../../assets/images/card_back.png";
import JOKER from "../../../assets/images/joker.png";
import TWO_C from "../../../assets/images/2C.png";
import TWO_D from "../../../assets/images/2D.png";
import TWO_H from "../../../assets/images/2H.png";
import TWO_S from "../../../assets/images/2S.png";
import THREE_C from "../../../assets/images/3C.png";
import THREE_D from "../../../assets/images/3D.png";
import THREE_H from "../../../assets/images/3H.png";
import THREE_S from "../../../assets/images/3S.png";
import FOUR_C from "../../../assets/images/4C.png";
import FOUR_D from "../../../assets/images/4D.png";
import FOUR_H from "../../../assets/images/4H.png";
import FOUR_S from "../../../assets/images/4S.png";
import FIVE_C from "../../../assets/images/5C.png";
import FIVE_D from "../../../assets/images/5D.png";
import FIVE_H from "../../../assets/images/5H.png";
import FIVE_S from "../../../assets/images/5S.png";
import SIX_C from "../../../assets/images/6C.png";
import SIX_D from "../../../assets/images/6D.png";
import SIX_H from "../../../assets/images/6H.png";
import SIX_S from "../../../assets/images/6S.png";
import SEVEN_C from "../../../assets/images/7C.png";
import SEVEN_D from "../../../assets/images/7D.png";
import SEVEN_H from "../../../assets/images/7H.png";
import SEVEN_S from "../../../assets/images/7S.png";
import EIGHT_C from "../../../assets/images/8C.png";
import EIGHT_D from "../../../assets/images/8D.png";
import EIGHT_H from "../../../assets/images/8H.png";
import EIGHT_S from "../../../assets/images/8S.png";
import NINE_C from "../../../assets/images/9C.png";
import NINE_D from "../../../assets/images/9D.png";
import NINE_H from "../../../assets/images/9H.png";
import NINE_S from "../../../assets/images/9S.png";
import TEN_C from "../../../assets/images/10C.png";
import TEN_D from "../../../assets/images/10D.png";
import TEN_H from "../../../assets/images/10H.png";
import TEN_S from "../../../assets/images/10S.png";
import JC from "../../../assets/images/JC.png";
import JD from "../../../assets/images/JD.png";
import JH from "../../../assets/images/JH.png";
import JS from "../../../assets/images/JS.png";
import QC from "../../../assets/images/QC.png";
import QD from "../../../assets/images/QD.png";
import QH from "../../../assets/images/QH.png";
import QS from "../../../assets/images/QS.png";
import KC from "../../../assets/images/KC.png";
import KD from "../../../assets/images/KD.png";
import KH from "../../../assets/images/KH.png";
import KS from "../../../assets/images/KS.png";
import AC from "../../../assets/images/AC.png";
import AD from "../../../assets/images/AD.png";
import AH from "../../../assets/images/AH.png";
import AS from "../../../assets/images/AS.png";

class Game extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            playersCanvasWidth: 800,
            playersCanvasHeight: 400,
            boardCanvasWidth: 800,
            boardCanvasHeight: 400,
        };

        this.topPadding = 50;
        this.leftPadding = 0;
        this.cardWidth = 75;
        this.cardHeight = 114;
        this.cardRowHeight = 130;
        this.playerInfoHeight = this.cardRowHeight;
        this.playerInfoWidth = 150;
        this.currentPlayerBarWidth = 30;

        // Bind functions so they can access 'this'
        this.updateCanvas = this.updateCanvas.bind(this);
        this.renderPlayers = this.renderPlayers.bind(this);
        this.renderBoard = this.renderBoard.bind(this);
        this.renderPlayerInfo = this.renderPlayerInfo.bind(this);
        this.renderPlayerCards = this.renderPlayerCards.bind(this);
        this.renderMultipleCardSets = this.renderMultipleCardSets.bind(this);
    }

    componentDidMount() {
        this.clearAndUpdateCanvas();
    }

    componentDidUpdate(prevProps) {
        console.log("props updated")
        this.clearAndUpdateCanvas();
    }

    clearAndUpdateCanvas() {
        var playersCtx = this.refs.playersCanvas.getContext("2d");
        var boardCtx = this.refs.boardCanvas.getContext("2d");
        this.clearCanvas(playersCtx);
        this.clearCanvas(boardCtx);
        this.updateCanvas(playersCtx, boardCtx);
    }

    /* Clear all the canvases */
    clearCanvas(ctx) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    }

    updateCanvas(playersCtx, boardCtx) {
        if (this.props.state != null) {
            // render the players to the players canvas
            this.renderPlayers(playersCtx, this.props.state.players);
            // render the board to the board canvas
            this.renderBoard(boardCtx, this.props.state);
        }
    }

    renderPlayers(ctx, players){
        // Render current player indicator
        this.renderCurrentPlayerIndicator(ctx, players);
        // Render background of players to match their team color
        this.renderPlayersBackgroundColor(ctx, players);
        for (var playerIdx in players) {
            var player = players[playerIdx];
            var x = this.playerInfoWidth + 10;
            var y = this.topPadding + 5 + (playerIdx * this.playerInfoHeight);
            // Render player info
            this.renderPlayerInfo(ctx, player, 0, y);
            // Render player hand cards
            this.renderPlayerCards(ctx, player, x, y);
        }
    }

    renderCurrentPlayerIndicator(ctx, players) {
        var y = this.topPadding;
        for (var player of players) {
            if (player.isCurrentPlayer) {
                ctx.fillStyle = "#078e2b";
                ctx.fillRect(0, y, this.currentPlayerBarWidth, this.playerInfoHeight)
                break
            } else {
                y += this.playerInfoHeight;
            }
        }
    }

    renderPlayersBackgroundColor(ctx, players) {
        var x = this.currentPlayerBarWidth;
        var y = this.topPadding;
        var bgWidth = this.playerInfoWidth - x;
        var bgHeight = this.playerInfoHeight;
        for (var player of players) {
            ctx.fillStyle = player.teamColor == "red" ? "#e4b9b9" : "#9dc4e0";
            ctx.fillRect(x, y, bgWidth, bgHeight);
            y += this.playerInfoHeight;
        }
    }

    renderPlayerInfo(ctx, player, x, y) {
        ctx.fillStyle = "#000000";
        ctx.font = "15px Arial";
        ctx.fillText("Player " + player.playerId, x + this.currentPlayerBarWidth + 10, y + 20);
        ctx.fillText("Human: " + player.isHuman.toString(), x + this.currentPlayerBarWidth + 10, y + 40);
        ctx.fillStyle = "#000000";
        ctx.font = "bold 15px Arial";
        ctx.fillText("Score: " + player.score.toString(), x + this.currentPlayerBarWidth + 10, y + 60);
    }

    renderPlayerCards(ctx, player, x, y) {
        // Separate the cards in the players hand by suit, assuming they are ordered
        var cardsBySuit = [];  // resulting List[List[card]] with lists of cards grouped by suit
        var sameSuitCards = {'cards': []};  // temporary list to hold cards of same suit while collecting them
        var previousCardSuit = null;  // suit of the last seen card to know when we've collected them all
        for (var card of player.cards) {
            if (card.suit != previousCardSuit) {  // Separate the cards by suit
                if (sameSuitCards.cards.length > 0) {
                    // Add the cards collected so far to the result list and start a new list of cards for the new suit
                    cardsBySuit.push(sameSuitCards)
                    sameSuitCards = {'cards': []};
                }
                previousCardSuit = card.suit;
            }
            sameSuitCards.cards.push(card);
        }
        // Don't forget to add the set of cards for the last suit
        if (sameSuitCards.cards.length > 0) {
            cardsBySuit.push(sameSuitCards)
        }
        this.renderMultipleCardSets(ctx, cardsBySuit, x, y);
    }

    renderBoard(ctx, state) {
        ctx.fillStyle = "#000000";
        ctx.font = "15px Arial";
        // Draw deck
        ctx.fillText("DECK", 100, 30);
        ctx.fillText("#cards: " + state.deck.numCards.toString(), 100, 50);
        var img = document.getElementById("card_back");
        ctx.drawImage(img, 100, 70, this.cardWidth, this.cardHeight);
        // Draw stack
        if (state.stack.topCard != null) {
            ctx.fillText("STACK", this.cardWidth + 150, 30);
            ctx.fillText("#cards: " + state.stack.numCards.toString(), this.cardWidth + 150, 50);
            var img = this.cardToImg(state.stack.topCard);
            ctx.drawImage(img, this.cardWidth + 150, 70, this.cardWidth, this.cardHeight);
        }
    }

    renderMultipleCardSets(ctx, cardSets, x, y, padding=10) {
        var cardX = x;  // first card is rendered exactly at X
        for (var cardSet of cardSets){
            var cardSetWidth = (cardSet.cards.length * this.cardWidth/4) + this.cardWidth/2
            if (cardX + cardSetWidth > ctx.canvas.width) {  // start a new row
                cardX = x;
                y += this.cardRowHeight;
            }
            for (var card of cardSet.cards){
                var img = this.cardToImg(card);
                // Draw the card at the current location
                ctx.drawImage(img, cardX, y, this.cardWidth, this.cardHeight);
                // Move a small bit to the right, so cards in the same set are slightly overlaid over each other
                cardX += this.cardWidth/4;
            }
            if ("highlight" in cardSet) {
                ctx.fillStyle = cardSet.highlight;
                ctx.fillRect(x, y, cardX - x, 10);
            }
            // Add extra spacing between card sets
            cardX += this.cardWidth * (5/6);
        }
    }

    cardToImg(card) {
        // Load card image to draw
        var imgName = card.isJoker ?  "joker" : card.shortRank + "" + card.shortSuit;
        return document.getElementById(imgName);
    }

    render() {
          return (
                     <div>
                         <div className={styles.flexContainer}>
                            <GameStateText state={this.props.state}/>
                         </div>

                         <div className={styles.flexContainer}>
                            <div className={styles.canvasContainerLeft}>
                                 <canvas ref="playersCanvas" id="playersCanvas"
                                         width={this.state.playersCanvasWidth+"px"}
                                         height={this.state.playersCanvasHeight+"px"}>
                                 </canvas>
                             </div>
                             <div className={styles.canvasContainerRight}>
                                 <canvas ref="boardCanvas" id="boardCanvas"
                                         width={this.state.boardCanvasWidth+"px"}
                                         height={this.state.boardCanvasHeight+"px"}>
                                 </canvas>
                             </div>
                         </div>
                         <img id="card_back" src={CARD_BACK} className={styles.hide}/>
                         <img id="2C" src={TWO_C} className={styles.hide}/>
                         <img id="2D" src={TWO_D} className={styles.hide}/>
                         <img id="2H" src={TWO_H} className={styles.hide}/>
                         <img id="2S" src={TWO_S} className={styles.hide}/>
                         <img id="3C" src={THREE_C} className={styles.hide}/>
                         <img id="3D" src={THREE_D} className={styles.hide}/>
                         <img id="3H" src={THREE_H} className={styles.hide}/>
                         <img id="3S" src={THREE_S} className={styles.hide}/>
                         <img id="4C" src={FOUR_C} className={styles.hide}/>
                         <img id="4D" src={FOUR_D} className={styles.hide}/>
                         <img id="4H" src={FOUR_H} className={styles.hide}/>
                         <img id="4S" src={FOUR_S} className={styles.hide}/>
                         <img id="5C" src={FIVE_C} className={styles.hide}/>
                         <img id="5D" src={FIVE_D} className={styles.hide}/>
                         <img id="5H" src={FIVE_H} className={styles.hide}/>
                         <img id="5S" src={FIVE_S} className={styles.hide}/>
                         <img id="6C" src={SIX_C} className={styles.hide}/>
                         <img id="6D" src={SIX_D} className={styles.hide}/>
                         <img id="6H" src={SIX_H} className={styles.hide}/>
                         <img id="6S" src={SIX_S} className={styles.hide}/>
                         <img id="7C" src={SEVEN_C} className={styles.hide}/>
                         <img id="7D" src={SEVEN_D} className={styles.hide}/>
                         <img id="7H" src={SEVEN_H} className={styles.hide}/>
                         <img id="7S" src={SEVEN_S} className={styles.hide}/>
                         <img id="8C" src={EIGHT_C} className={styles.hide}/>
                         <img id="8D" src={EIGHT_D} className={styles.hide}/>
                         <img id="8H" src={EIGHT_H} className={styles.hide}/>
                         <img id="8S" src={EIGHT_S} className={styles.hide}/>
                         <img id="9C" src={NINE_C} className={styles.hide}/>
                         <img id="9D" src={NINE_D} className={styles.hide}/>
                         <img id="9H" src={NINE_H} className={styles.hide}/>
                         <img id="9S" src={NINE_S} className={styles.hide}/>
                         <img id="10C" src={TEN_C} className={styles.hide}/>
                         <img id="10D" src={TEN_D} className={styles.hide}/>
                         <img id="10H" src={TEN_H} className={styles.hide}/>
                         <img id="10S" src={TEN_S} className={styles.hide}/>
                         <img id="JC" src={JC} className={styles.hide}/>
                         <img id="JD" src={JD} className={styles.hide}/>
                         <img id="JH" src={JH} className={styles.hide}/>
                         <img id="JS" src={JS} className={styles.hide}/>
                         <img id="QC" src={QC} className={styles.hide}/>
                         <img id="QD" src={QD} className={styles.hide}/>
                         <img id="QH" src={QH} className={styles.hide}/>
                         <img id="QS" src={QS} className={styles.hide}/>
                         <img id="KC" src={KC} className={styles.hide}/>
                         <img id="KD" src={KD} className={styles.hide}/>
                         <img id="KH" src={KH} className={styles.hide}/>
                         <img id="KS" src={KS} className={styles.hide}/>
                         <img id="AC" src={AC} className={styles.hide}/>
                         <img id="AD" src={AD} className={styles.hide}/>
                         <img id="AH" src={AH} className={styles.hide}/>
                         <img id="AS" src={AS} className={styles.hide}/>
                         <img id="joker" src={JOKER} className={styles.hide}/>
                      </div>
                 )
        }
};

function GameStateText(props) {
    if (props.state != null){
        var topCard = props.state.stack.topCard != null ? props.state.stack.topCard.rank + "" + props.state.stack.topCard.suit : "empty";
        return (<div className={styles.gameStateContainer}>
                  <ul>
                      <li>PHASE: {props.state.phase}</li>
                      <li>FINISHED: {props.state.isFinished.toString()}</li>
                      <li>DECK: {props.state.deck.numCards} cards</li>
                      <li>STACK: {props.state.stack.numCards} cards | top = ({topCard})</li>
                  </ul>
                </div>);
    }
    return null;
}

// Make this component available to other components
export default Game;
