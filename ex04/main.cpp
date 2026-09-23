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

	std::string s1 = argv[2];
	std::string s2 = argv[3];

	if (s1.empty())
	{
		std::cerr << "Error: s1 cannout be empty" << std::endl;
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

	std::string result;
	std::string::size_type pos = 0;
	std::string::size_type found;

	while ((found = content.find(s1, pos)) != std::string::npos)
	{
		result += content.substr(pos, found - pos);
		result += s2;
		pos = found + s1.length();
	}

	result += content.substr(pos);

	std::cout << content;

	return 0;
}