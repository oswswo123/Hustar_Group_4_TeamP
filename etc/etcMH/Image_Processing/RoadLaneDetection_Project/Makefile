CC = g++
PROJECT = output
SRC = RoadDetection_HSV.cpp
LIBS = `pkg-config --cflags --libs opencv`
$(PROJECT) : $(SRC)
	$(CC) $(SRC) -o $(PROJECT) $(LIBS)
	./$(PROJECT)
