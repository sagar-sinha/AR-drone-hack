var arDrone = require('ar-drone');

var client  = arDrone.createClient();
client.createRepl();
client.disableEmergency();

var stdin = process.stdin;
stdin.setRawMode(true);
stdin.resume();
stdin.setEncoding('utf8');

stdin.on('data', function(key) {
	if(key == '\u0003') {
		process.stdout.write('Bye!\n');
		client.land();
		process.exit();
	}
	else if(key == '\u0020') {
		client.stop();
		process.stdout.write('Hovering\n');
	} 
	// t for takeoff
	else if (key == '\u0074') {
		client.takeoff();
		process.stdout.write('Taking off.\n');
	}
	// l for landing
	else if (key == '\u006C') {
		client.land();
		process.stdout.write('Landing.\n');
	}
	// forward (w)
	else if (key == '\u0077') {
		client.front(0.2);
        process.stdout.write('Moving forward.\n'); 
    }
	// backward (s)
	else if (key == '\u0073') {
		client.back(0.2);
        process.stdout.write('Moving backwards.\n'); 
    }
	// left (a)
	else if (key == '\u0061') {
		client.left(0.2);
        process.stdout.write('Moving left.\n'); 
    }
	// right (d)
	else if (key == '\u0064') {
		client.right(0.2);
        process.stdout.write('Moving right.\n'); 
    }
	// up (up arrow)
	else if (key == '\u001B\u005B\u0041') {
		client.up(0.2);
        process.stdout.write('Moving up.\n'); 
    }
	// down (down arrow)
    else if (key == '\u001B\u005B\u0042') {
		client.down(0.2);
        process.stdout.write('Moving down.\n'); 
    }
	// rotate cw (right arrow)
    else if (key == '\u001B\u005B\u0043') {
		client.clockwise(0.3);
        process.stdout.write('Rotating cw.\n'); 
    }
	// rotate ccw (left arrow)
    else if (key == '\u001B\u005B\u0044') {
		client.clockwise(-0.3);
        process.stdout.write('Rotating ccw.\n'); 
    }
});
