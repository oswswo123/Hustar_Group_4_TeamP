CC = g++
PROJECT = output
SRC = Homework2-2,3.cpp
LIBS = `pkg-config --cflags --libs opencv`
$(PROJECT) : $(SRC)
	$(CC) $(SRC) -o $(PROJECT) $(LIBS)
	./$(PROJECT)
