#include <iostream>
#include <string>
#include <fstream>

int main(int argc, char **argv)
{
	if (argc != 4)
	{
		std::cerr << "Usage: ./replace <filename> <s1> <s2>" << std::endl;
		return 1;
	}

	std::ifstream input(argv[1]);

	if (!input.is_open())
	{
		std::cerr << "Error: cannot open input file" << std::endl;
		return 1;
	}

	std::string content;
	std::string line;

	while (std::getline(input, line))
	{
		content += line;
		if (!input.eof())
			content += "\n";
	}
	
	input.close();

	std::cout << content;

	return 0;
}