#include "Harl.hpp"

int main(int argc, char **argv)
{
	if (argc != 2)
		return 1;

	std::string levels[4] = {
		"DEBUG",
		"INFO",
		"WARNING",
		"ERROR"
	};

	int level = -1;

	for (int i = 0; i < 4; i++)
	{
		if (argv[1] == levels[i])
			level = i;
	}

	Harl harl;
	int start;

	switch (level)
	{
	case 0:
		start = 0;
		break;
	case 1:
		start = 1;
		break;
	case 2:
		start = 2;
		break;
	case 3:
		start = 3;
		break;
	default:
		std::cout
			<< "[ Probably complaining about insignificant problems ]"
			<< std::endl;
		return 0;
	}

	for (int i = start; i < 4; i++)
		harl.complain(levels[i]);

	return 0;
}
