sort: main.o battle.o
	gcc main.o battle.o -o main
sort.o: main.c
	gcc -Wall -Werror -pedantic-errors -c main.c
sorts.o: battle.c main.h
	gcc -Wall -Werror -pedantic-errors -c battle.c
clean:
	rm -f *.o main main.exe
