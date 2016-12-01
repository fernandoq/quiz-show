var baseUrl =  'http://192.168.42.73:8000',
    team,
    correctQuestion,
    otherQuestions = [],
    randomPositionOfAnswer,
    startTime,
    duration,
    redScore,
    blueScore;

function joinTeam(teamName) {
    team = teamName;
    if (teamName === 'blue') {
    	teamName = 'green';
    }
    $('.team-name-sub-header').html(teamName + ' team').css('color', teamName);
    $.ajax({
        url: baseUrl + '/join/' + team,
        type: 'GET',
        success: function(data) {
            //alert('You joined the ' + team + 'team');
            $('.header').html('Waiting for round to start');
            getRound();
        },
        fail: function(data) {
            //alert('You failed the ' + team + 'team');
            getRound();
        },
        error: function(data) {
            //alert('You errored the ' + team + 'team');
            $('.header').html('Waiting for next round to start');
            getRound();
        }
    });
}

function getRound() {
    var seconds;
    // GET round data and transfer to new html page.
    $.ajax({
        url: baseUrl + '/getRound',
        type: 'GET',
        success: function(data) {
            //alert('You got a round');
            setRoundUp(data);
        },
        fail: function(data) {
            //alert('You failed to get a round');
            setRoundUp('fail');
        },
        error: function(data) {
            //alert('You errored to get a round');
            // Mocking endpoint
            data.roundDuration = 30;
            data.startTime = new Date();
            // logging
            window.console.log(data.startTime.getHours() + ':' + data.startTime.getMinutes() + ':' + data.startTime.getSeconds());
            // 5 seconds
            seconds = data.startTime.getSeconds() + 5;
            data.startTime = (data.startTime).setSeconds(seconds);
            data.correctAnswer = 'Nick Drake - Shramp song';
            data.wrongAnswers = [
                'Nob Bob - Fake song',
                'Lob Bob - Fake song 2',
                'Grok Bob - Fake song 3'
            ];
            data.redScore = 27;
            data.blueScore = 33;
            setRoundUp(data);
        }
    });
}

function setRoundUp(data) {
    var i = 0,
    numOfAnswers = data.wrongAnswers.length + 1;
    randomPositionOfAnswer = Math.floor(Math.random() * numOfAnswers-1) + 1,
    htmlForButtons = '',
    htmlForButton = '',
    iAnswerIsCorrect = false,
    answersToDisplay = [],
    millisecondsUntilRoundStarts = 0,
    scoreText = '';

    // NOTE: data.wrongAnswers will now contain the correct answer
    data.wrongAnswers.splice(randomPositionOfAnswer, 0, data.correctAnswer);
    // for code readability.
    answersToDisplay = data.wrongAnswers,
    startTime = new Date(data.startTime);

    redScore = data.redScore;
    blueScore = data.blueScore;

    for(i=0; i < answersToDisplay.length; i++) {
        iAnswerIsCorrect = answersToDisplay[i] === data.correctAnswer;
        htmlForButton = '<div class="row"><div class="col-md-12">'+
            '<button style="margin-bottom: 5px;" class="btn-lg question-btn btn-default" onClick="answerQuestion('+iAnswerIsCorrect+')">'+ answersToDisplay[i] +'</button></div></div>';
        htmlForButtons += htmlForButton;
    }

    $('.next-round-timer').html('Round will begin at ' + startTime.getHours() + ':' + (startTime.getMinutes()<10?'0':'') + startTime.getMinutes() + ':' + (startTime.getSeconds()<10?'0':'') + startTime.getSeconds());
    millisecondsUntilRoundStarts = startTime.getTime() - (new Date()).getTime();
    $('.content').html('');

    if (team === 'blue') {
        scoreText = 'Green: ' + blueScore + ' Red: ' + redScore;
    } else {
        scoreText = 'Red: ' + redScore + ' Green: ' + blueScore;
    }

    $('.score-sub-header').html(scoreText);

    // TODO: if the player doesn't vote, call next round a few seconds before roundDuration expires

    return setTimeout(function() {
        $('.next-round-timer').html('');
        $('.header').html();
        $('.content').html(htmlForButtons);
    }, millisecondsUntilRoundStarts);
}

function answerQuestion(correct) {
    if (correct) {
        $.ajax({
            url: baseUrl + '/correct/' + team,
            type: 'GET',
            success: function(data) {
                //alert('You joined the ' + team + 'team');
                answerSubmitted(correct);
            },
            fail: function(data) {
                //alert('You failed the ' + team + 'team');
                //getRound();
            },
            error: function(data) {
                //alert('You errored the ' + team + 'team');
                answerSubmitted(correct);
            }
        });
    } else {
        answerSubmitted(correct);
    }
}

function answerSubmitted(correct) {
    var correctAnswer;
    if (correct) {
        correctAnswer = "You're correct!";
    } else {
        correctAnswer = "You're wrong";
    }
    $('.header').html(correctAnswer);
    $('.question-btn').prop('disabled', true);

    // After you submit an answer get the next round
    getRound();
}
