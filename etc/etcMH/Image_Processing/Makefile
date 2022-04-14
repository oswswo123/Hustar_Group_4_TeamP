CC = g++
PROJECT = output
SRC = Homework3-4.cpp
LIBS = `pkg-config --cflags --libs opencv`
$(PROJECT) : $(SRC)
	$(CC) $(SRC) -o $(PROJECT) $(LIBS)
	./$(PROJECT)
