#include <iostream>
#include <string>

int main(int argc, char **argv)
{
	if (argc != 4)
	{
		std::cerr << "Usage: ./replace <filename> <s1> <s2>" << std::endl;
		return 1;
	}

	std::cout << "filename: " << argv[1] << std::endl;
	std::cout << "s1: " << argv[2] << std::endl;
	std::cout << "s2: " << argv[3] << std::endl;

	return 0;
}