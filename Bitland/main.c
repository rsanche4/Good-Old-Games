/*
 * BITLAND
 * CREATED BY @RSANCHE4
 * Here you will find the code for the game.
 *
 */
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>
#include <termios.h>
#include "main.h"

//Constants
#define WID 20
#define HEI 50
#define ENCOUNTER 250

//Global variables
//When the game is over, it will be 1.
int game_is_done = 0;

//This helps with making sure when we are in a village we don't encounter anything
int in_village = 0;

//This is the plane. Change WID or HEI to change the width and its height
char plane[WID][HEI];

//This contains the hidden location of the asterisk, food.
int array_of_coord[6];
int array_food[2];

//This will just make the food gone when taken
int food_found;

void game_won() {
	system("clear");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("################ PLAYER WON!! ###############\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("HP:%d/%d | ATK:%d | FOOD:%d | LEVEL:%d\n", hp, maxhp, atk, food, level);
	game_is_done = 1;
}

void game_over() {
	system("clear");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("################ GAME IS OVER ###############\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("HP:0/%d | ATK:%d | FOOD:%d | LEVEL:%d\n", maxhp, atk, food, level);
	game_is_done = 1;
}

//This will enable Raw Mode, which allows us to see all key presses of user
struct termios orig_termios;
void disableRawMode() {
	tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios);
}
void enableRawMode() {
	tcgetattr(STDIN_FILENO, &orig_termios);
	atexit(disableRawMode);
	struct termios raw = orig_termios;
	raw.c_lflag &= ~(ECHO | ICANON);
	tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}

//Displays everything. The UI, the plane, the inputs, etc
void display() {
	system("clear");
	printf("HP:%d/%d      ATK:%d       FOOD:%d       LEVEL:%d\n", hp, maxhp, atk, food, level);
	for (int i = 0; i < WID; i++) {
		for (int j = 0; j < HEI; j++) {
			if (plane[i][j] == '@') {
				printf("\033[0;32m");
				printf("%c", plane[i][j]);
				printf("\033[0;37m");
			} else if (plane[i][j] == '&') {
				printf("\033[0;33m");
				printf("%c", plane[i][j]);
				printf("\033[0;37m");
			} else if (plane[i][j] == '*') {
				printf("\033[0;31m");
				printf("%c", plane[i][j]);
				printf("\033[0;37m");
			} else {
				printf("%c", plane[i][j]);
			}
			if (j == HEI-1) {
				printf("\n");
			}
		}
	}
	printf("Keys:                              Map Legend:\n");
	printf("Press w to move up.                & - Food\n");
	printf("Press a to move left.\n");
	printf("Press s to move down.              * - Level up\n");
	printf("Press d to move right.\n");
	printf("Press e to eat.\n");

}

//Small function to draw houses in map
void draw_house(int a, int b) {
	plane[a][b] = '#';
	plane[a-1][b] = '#';
	plane[a][b+2] = '#';
	plane[a-1][b+2] = '#';
	plane[a-1][b+1] = '#';
	plane[a-1][b-1] = '#';
	plane[a-1][b+3] = '#';
	plane[a-2][b] = '#';
	plane[a-2][b+1] = '#';
	plane[a-2][b+2] = '#';
	plane[a-3][b+1] = '#';
}

void load_town() {
	//Regenerate the life of the player
	hp = maxhp;
	in_village = 1;
	for (int i = 0; i < WID; i++) {
		for (int j = 0; j < HEI; j++) {
			//generate the border
			if (i == 0 || i == 19 || j == 0 || j == 49) {
				plane[i][j] = '#';
			} else {
				plane[i][j] = ' ';
			}
		}
	}

	//Draw the town
	draw_house(9, 7);
	draw_house(16, 7);

	draw_house(9, 40);
	draw_house(16, 40);

	//Initialize the player
	plane[WID-5][HEI/2] = '@';
	plane[WID/2][HEI/2] = '&';

	plane[2][HEI/2] = '*';

	display();

}

void load_maze() {
	in_village = 0;
	for (int i = 0; i < WID; i++) {
		for (int j = 0; j < HEI; j++) {
			//generate the border
			if (i == 0 || i == 19 || j == 0 || j == 49) {
				plane[i][j] = '#';
			} else {
				plane[i][j] = ' ';
			}
		}
	}

	//This starts generating random values
	int random_val[HEI/4];
	time_t t;
	srand((unsigned) time(&t));
	for (int i = 1; i < WID-1; i++) {
		//Generate random values from 1 to HEI-1 (because we have a border we don't count the last)
		for (int k = 0; k < HEI/4; k++) {
			random_val[k] = rand() % ((HEI-1) + 1 - 1) + 1;
		}
		for (int h = 0; h < HEI/4; h++) {
			plane[i][random_val[h]] = '#';
		}
	}
	plane[WID/2][HEI/2] = '@';

	//Here we are generating the hidden coordinates for the * (Exit) inside the array_of_coord. There are 3 *'s in the map.
	array_of_coord[0] = rand() % ((WID-2) + 1 - 1) + 1;
	array_of_coord[1] = rand() % ((HEI-2) + 1 - 1) + 1;
	array_of_coord[2] = rand() % ((WID-2) + 1 - 1) + 1;
	array_of_coord[3] = rand() % ((HEI-2) + 1 - 1) + 1;
	array_of_coord[4] = rand() % ((WID-2) + 1 - 1) + 1;
	array_of_coord[5] = rand() % ((HEI-2) + 1 - 1) + 1;

	//Here we are generating the hidden coordinates for the food.
	array_food[0] = rand() % ((WID-2) + 1 - 1) + 1;
	array_food[1] = rand() % ((HEI-2) + 1 - 1) + 1;

	food_found = 0;

	display();

}

//Should check if our level is a town or a maze. This will be run again and again to initialize the level.
void game_init() {

	if (level % 5 == 0) {
		load_town();
	} else {
		load_maze();
	}
}

//Will check if an asterisk is in range
int lvlup_in_range(int a, int b, int playeri, int playerj) {
	if ((playeri+a == array_of_coord[0] && playerj+b == array_of_coord[1]) ||
			(playeri+a == array_of_coord[2] && playerj+b == array_of_coord[3]) ||
			(playeri+a == array_of_coord[4] && playerj+b == array_of_coord[5])) {
		return 1;
	}
	return 0;
}

//Will check if the food is in range
int food_in_range(int a, int b, int playeri, int playerj) {
	if (playeri+a == array_food[0] && playerj+b == array_food[1]) {
		return 1;
	}
	return 0;
}

//Here I am just copying over the keys into one function that will do most of the work
void redraw_helper(int a, int b) {
		//First find the player in the plane
		int playeri = 0;
		int playerj = 0;
		for (int i = 0; i < WID; i++) {
			for (int j = 0; j < HEI; j++) {
				if (plane[i][j] == '@') {
					playeri = i;
					playerj = j;
				}
			}
		}
		//find the food position
		int foodi = 0;
		int foodj = 0;
		for (int i = 0; i < WID; i++) {
			for (int j = 0; j < HEI; j++) {
				if (plane[i][j] == '&') {
					foodi = i;
					foodj = j;
				}
			}
		}

		//Then check that next up isn't a boundary
		if (plane[playeri+a][playerj+b] != '#') {
			plane[playeri][playerj] = '.';
			plane[playeri+a][playerj+b] = '@';
			display();
		}
		//Did we find food? Show it.
		if (food_in_range(a*4, b*4, playeri, playerj) && !food_found) {
			plane[playeri+(a*4)][playerj+(b*4)] = '&';
			food_found = 1;
			display();
		}
		if (food_in_range(a*3, b*3, playeri, playerj) && !food_found) {
			plane[playeri+(a*3)][playerj+(b*3)] = '&';
			food_found = 1;
			display();
		}
		if (food_in_range(a*2, b*2, playeri, playerj) && !food_found) {
			plane[playeri+(a*2)][playerj+(b*2)] = '&';
			food_found = 1;
			display();
		}
	
		//Did we just walk over one of the foods?
		if (playeri+a == foodi && playerj+b == foodj) {
			plane[playeri][playerj] = '.';
			time_t t;
			srand((unsigned) time(&t));
			food += rand() % 7;
			display();
		}
		//This will check that the asterisk hidden is not hidden anymore
		if (lvlup_in_range(a*4, b*4, playeri, playerj) && !in_village) {
			plane[playeri+(a*4)][playerj+(b*4)] = '*';
			display();
		}
		if (lvlup_in_range(a*3, b*3, playeri, playerj) && !in_village) {
			plane[playeri+(a*3)][playerj+(b*3)] = '*';
			display();
		}
		if (lvlup_in_range(a*2, b*2, playeri, playerj) && !in_village) {
			plane[playeri+(a*2)][playerj+(b*2)] = '*';
			display();
		}

		//This will make sure to move us up a level if we did in fact find the asterisk
		if (!in_village && ((playeri == array_of_coord[0] && playerj == array_of_coord[1]) ||
				(playeri == array_of_coord[2] && playerj == array_of_coord[3]) ||
				(playeri == array_of_coord[4] && playerj == array_of_coord[5]))) {
			level += 1;
			maxhp += 1;
			hp += 1;
			atk += 1;
			game_init();
		}
		if (level % 5 == 0 && playeri == 2 && playerj == HEI/2) {
			level += 1;
			game_init();
		}
}

void redraw(char c) {
	int battle_result = 0;
	if (!in_village) {
		time_t t;
		srand((unsigned) time(&t));
		if (level > 60) {
			disableRawMode();
			battle_result = battle();
			enableRawMode();
		}
		int random_encounter = rand() % ENCOUNTER;
		//this will only run when we are not at the last level
		if (random_encounter < 10 && level < 60) {
			disableRawMode();
			battle_result = battle(); //battle returns 0 if battle was successful, a 1 if the player died, thus game over, 2 if we won the game
			enableRawMode();
		}
		if (battle_result == 1) {
			game_over();
			return;
		} else if (battle_result == 2) {
			game_won();
			return;
		}

	}

	if (c == 'w') {
		redraw_helper(-1, 0); //the numbers mean the values to look for. If we are looking up, then that's -1, 0.
	}
	if (c == 's') {
		redraw_helper(1, 0);
	}
	if (c == 'a') {
		redraw_helper(0, -1);
	}
	if (c == 'd') {
		redraw_helper(0, 1);
	}
	if (c == 'e' && food > 0 && hp != maxhp) {
		//If player wants to eat, then max out the hp
		food--;
		hp = maxhp;
		display();
	}
}

//Main Menu Prompt. This checks as well if the player pressed Enter and if they did, we start the game.
void menu() {
	system("clear");
	int title_count = 0;
	int start_count = 0;
	int exit_count = 0;
	int dev_count = 0;
	for (int i = 0; i < WID; i++) {
		for (int j = 0; j < HEI; j++) {
			if (i == 0 || i == 1 || i == 18 || i == 19) {
				putchar('#');
			}
			if (i == 7 && !title_count) {
				for (int k = 0; k < 21; k++) {
					putchar(' ');
				}
				printf("\033[0;33m");
				printf("BITLAND");
				printf("\033[0;37m");
				title_count = 1;
			}
			if (i == 11 && !start_count) {
				for (int k = 0; k < 15; k++) {
					putchar(' ');
				}
				printf("\033[0;33m");
				printf("PRESS ENTER TO START");
				printf("\033[0;37m");
				start_count = 1;
			}
			if (i == 13 && !exit_count) {
				for (int k = 0; k < 16; k++) {
					putchar(' ');
				}
				printf("\033[0;33m");
				printf("PRESS ESC TO EXIT");
				printf("\033[0;37m");
				exit_count = 1;
			}
			if (i == 15 && !dev_count) {
				for (int k = 0; k < 20; k++) {
					putchar(' ');
				}
				printf("\033[0;33m");
				printf("@rsanche4");
				printf("\033[0;37m");
				dev_count = 1;
			}
			if (j == HEI-1) {
				printf("\n");
			}
		}
	}
}

int main() {
	//Init the stats
	hp = 10;
	maxhp = 10;
	food = 0;
	atk = 5;
	level = 0;
	menu();
	enableRawMode();
	char c;
	int esc_value = 27;
	int enter_value = 10;
	int game_started = 0;

	while (read(STDIN_FILENO, &c, 1) == 1 && c != esc_value) {
		if (c == enter_value && !game_started) {
			game_started = 1;
			game_init();
		}
		if (c == 'w' && game_started) {
			redraw(c);
			if (game_is_done) {
				break;
			}
		}
		if (c == 's' && game_started) {
			redraw(c);
			if (game_is_done) {
				break;
			}
		}
		if (c == 'a' && game_started) {
			redraw(c);
			if (game_is_done) {
				break;
			}
		}
		if (c == 'd' && game_started) {
			redraw(c);
			if (game_is_done) {
				break;
			}
		}
		if (c == 'e' && game_started) {
			redraw(c);
			if (game_is_done) {
				break;
			}
		}
	}

	return EXIT_SUCCESS;
}

