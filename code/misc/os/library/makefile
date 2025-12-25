# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -g -I include
LDFLAGS = -lpthread

# Directories
SRC_DIR = src
BUILD_DIR = build

# Source files and objects
SRCS = $(SRC_DIR)/library.c $(SRC_DIR)/main.c
OBJS = $(BUILD_DIR)/library.o $(BUILD_DIR)/main.o

# Target executable
TARGET = library

# Default target
all: $(BUILD_DIR) $(TARGET)

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Link object files to create executable
$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $@ $(LDFLAGS)

# Compile source files to object files
$(BUILD_DIR)/library.o: $(SRC_DIR)/library.c include/library.h
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.c include/library.h
	$(CC) $(CFLAGS) -c $< -o $@

# Build the standalone signal.c (single file version)
singal: singal.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

lru: lru.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR) $(TARGET) singal lru

# Run the program
run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run singal
