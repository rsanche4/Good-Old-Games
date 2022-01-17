/*
 * battle.c
 *
 *
 * Author: @rsanche4
 * Battle.c runs when we encounter an enemy.
 */
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>
#include <termios.h>
#include "main.h"

#define MAX_LEN 128

//this is important when determining if the game is over
int turn_result = 0;

//Here I am defining all the enemies stats
const int cute_spider_hp = 9;
const int cute_spider_atk = 4;
const int timid_mouse_hp = 13;
const int timid_mouse_atk = 8;
const int big_scorpion_hp = 17;
const int big_scorpion_atk = 12;
const int angry_bat_hp = 21;
const int angry_bat_atk = 16;
const int hungry_bear_hp = 25;
const int hungry_bear_atk = 20;
const int lone_wolf_hp = 29;
const int lone_wolf_atk = 24;
const int giant_roach_hp = 33;
const int giant_roach_atk = 28;
const int dead_walker_hp = 37;
const int dead_walker_atk = 32;
const int lost_soul_hp = 41;
const int lost_soul_atk = 36;
const int pretty_fairy_hp = 45;
const int pretty_fairy_atk = 40;
const int poor_devil_hp = 49;
const int poor_devil_atk = 44;
const int creepy_cyclop_hp = 53;
const int creepy_cyclop_atk = 48;
const int grim_reaper_hp = 60;
const int grim_reaper_atk = 50;


void enem_desc() {
	if (level < 5) {
		printf("The cute spider is making some webs...\n");
	} else if (level > 5 && level < 10) {
		printf("The timid mouse is too timid to approach.\n");
	} else if (level > 10 && level < 15) {
		printf("The big scorpion is suspiciously quiet.\n");
	} else if (level > 15 && level < 20) {
		printf("This angry bat surely hates your luck!\n");
	} else if (level > 20 && level < 25) {
		printf("The hungry bear is looking for something to eat...\n");
	} else if (level > 25 && level < 30) {
		printf("The lone wolf sure likes your company!\n");
	} else if (level > 30 && level < 35) {
		printf("The giant roach is approaching. Really! A giant roach!\n");
	} else if (level > 35 && level < 40) {
		printf("The dead walker wants to turn you into another of his kind!\n");
	} else if (level > 40 && level < 45) {
		printf("The lost soul hovers in place... lost.\n");
	} else if (level > 45 && level < 50) {
		printf("The pretty fairy is making your heart skip a beat.\n");
	} else if (level > 50 && level < 55) {
		printf("The poor devil is trying to stay out trouble...\n");
	} else if (level > 55 && level < 60) {
		printf("The creepy cyclop stares at you... intensely.\n");
	} else if (level > 60) {
		printf("The grim reaper wants to finish your game!!\n");
	}
}

//Prints the ascii art of the monsters
void print_image(FILE *fptr)
{
	char read_string[MAX_LEN];

	while(fgets(read_string,sizeof(read_string),fptr) != NULL)
		printf("%s",read_string);
}

//Once the battle began, we take turns. 1 means the turn of the player, 0 means the turn of the monster.
void turns(int player_turn, int enem_hp, int enem_atk) {
	while (true) {
		if (player_turn == 1) {
			system("clear");
			sleep(1);
			system("clear");

			char *filename;
			if (level < 5) {
				filename = "cute_spider.txt";
			} else if (level > 5 && level < 10) {
				filename = "timid_mouse.txt";
			} else if (level > 10 && level < 15) {
				filename = "big_scorpion.txt";
			} else if (level > 15 && level < 20) {
				filename = "angry_bat.txt";
			} else if (level > 20 && level < 25) {
				filename = "hungry_bear.txt";
			} else if (level > 25 && level < 30) {
				filename = "lone_wolf.txt";
			} else if (level > 30 && level < 35) {
				filename = "giant_roach.txt";
			} else if (level > 35 && level < 40) {
				filename = "dead_walker.txt";
			} else if (level > 40 && level < 45) {
				filename = "lost_soul.txt";
			} else if (level > 45 && level < 50) {
				filename = "pretty_fairy.txt";
			} else if (level > 50 && level < 55) {
				filename = "poor_devil.txt";
			} else if (level > 55 && level < 60) {
				filename = "creepy_cyclop.txt";
			} else if (level > 60) {
				filename = "grim_reaper.txt";
			}
			FILE *fptr = NULL;
			if((fptr = fopen(filename,"r")) == NULL)
			{
				fprintf(stderr,"error opening %s\n",filename);
			}
			print_image(fptr);
			fclose(fptr);
			printf("\n");

			printf("\n");

			printf("|  Enemy HP: %d  |  Enemy ATK: %d  |\n", enem_hp, enem_atk);
			printf("|  Your HP: %d/%d  |  Your ATK: %d  |  Your FOOD: %d  |\n", hp, maxhp, atk, food);
			enem_desc();
			printf("What would you like to do? Enter F to attack, or E to eat food: \n");
			char input;
			scanf("%c", &input);
			time_t t;
			srand((unsigned) time(&t));
			if (input == 'f' || input == 'F') {
				int attack = rand() % atk;
				enem_hp = enem_hp - attack;
				system("clear");

				printf("You dealt %d damage to the enemy!\n", attack);
				sleep(2);
				if (enem_hp <= 0) {

					printf("The enemy lost and ran away...\n");
					sleep(2);

					turn_result = 0;
					if (level > 60) {
						turn_result = 2;
					}
					return;
				} else if (enem_hp > 0) {
					player_turn = 0;
				}
			} else if (input == 'e' || input == 'E') {
				if (food > 0) {
					food--;
					hp = maxhp;
					system("clear");
					sleep(2);
					printf("You ate a bit and now you feel healthier. Your HP is maxed out!\n");
					sleep(2);
				}
				player_turn = 0;
			}
		}
		if (player_turn == 0) {
			system("clear");
			sleep(1);
			system("clear");

			char *filename;
			if (level < 5) {
				filename = "cute_spider.txt";
			} else if (level > 5 && level < 10) {
				filename = "timid_mouse.txt";
			} else if (level > 10 && level < 15) {
				filename = "big_scorpion.txt";
			} else if (level > 15 && level < 20) {
				filename = "angry_bat.txt";
			} else if (level > 20 && level < 25) {
				filename = "hungry_bear.txt";
			} else if (level > 25 && level < 30) {
				filename = "lone_wolf.txt";
			} else if (level > 30 && level < 35) {
				filename = "giant_roach.txt";
			} else if (level > 35 && level < 40) {
				filename = "dead_walker.txt";
			} else if (level > 40 && level < 45) {
				filename = "lost_soul.txt";
			} else if (level > 45 && level < 50) {
				filename = "pretty_fairy.txt";
			} else if (level > 50 && level < 55) {
				filename = "poor_devil.txt";
			} else if (level > 55 && level < 60) {
				filename = "creepy_cyclop.txt";
			} else if (level > 60) {
				filename = "grim_reaper.txt";
			}
			FILE *fptr = NULL;
			if((fptr = fopen(filename,"r")) == NULL)
			{
				fprintf(stderr,"error opening %s\n",filename);
			}
			print_image(fptr);
			fclose(fptr);
			printf("\n");

			printf("\n");

			printf("|  Enemy HP: %d  |  Enemy ATK: %d  |\n", enem_hp, enem_atk);
			printf("|  Your HP: %d/%d  |  Your ATK: %d  |  Your FOOD: %d  |\n", hp, maxhp, atk, food);
			enem_desc();
			time_t t;
			srand((unsigned) time(&t));
			int random_attack = rand() % enem_atk;
			hp = hp - random_attack;
			system("clear");
			//sleep(2);
			printf("Enemy dealt %d damage to you!\n", random_attack);
			sleep(2);
			if (hp <= 0) {
				turn_result = 1;
				return;
			} else if (hp > 0) {
				player_turn = 1;
			}
		}
	}
}



int battle() {
	system("clear");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("################ BATTLE TIME! ###############\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	printf("#############################################\n");
	sleep(3);
	if (level < 5) {
		turns(1, cute_spider_hp, cute_spider_atk);
		return turn_result;
	} else if (level > 5 && level < 10) {
		turns(1, timid_mouse_hp, timid_mouse_atk);
		return turn_result;
	} else if (level > 10 && level < 15) {
		turns(1, big_scorpion_hp, big_scorpion_atk);
		return turn_result;
	} else if (level > 15 && level < 20) {
		turns(1, angry_bat_hp, angry_bat_atk);
		return turn_result;
	} else if (level > 20 && level < 25) {
		turns(1, hungry_bear_hp, hungry_bear_atk);
		return turn_result;
	} else if (level > 25 && level < 30) {
		turns(1, lone_wolf_hp, lone_wolf_atk);
		return turn_result;
	} else if (level > 30 && level < 35) {
		turns(1, giant_roach_hp, giant_roach_atk);
		return turn_result;
	} else if (level > 35 && level < 40) {
		turns(1, dead_walker_hp, dead_walker_atk);
		return turn_result;
	} else if (level > 40 && level < 45) {
		turns(1, lost_soul_hp, lost_soul_atk);
		return turn_result;
	} else if (level > 45 && level < 50) {
		turns(1, pretty_fairy_hp, pretty_fairy_atk);
		return turn_result;
	} else if (level > 50 && level < 55) {
		turns(1, poor_devil_hp, poor_devil_atk);
		return turn_result;
	} else if (level > 55 && level < 60) {
		turns(1, creepy_cyclop_hp, creepy_cyclop_atk);
		return turn_result;
	} else if (level > 60) {
		turns(0, grim_reaper_hp, grim_reaper_atk);
		return turn_result;
	}
	return turn_result;

}
