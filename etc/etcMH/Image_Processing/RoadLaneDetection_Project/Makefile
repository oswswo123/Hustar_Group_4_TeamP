CC = g++
PROJECT = output_Binary
SRC = RoadDetection_Binary.cpp
LIBS = `pkg-config --cflags --libs opencv`
$(PROJECT) : $(SRC)
	$(CC) $(SRC) -o $(PROJECT) $(LIBS)
	./$(PROJECT)
