#include "Zombie.hpp"

int main(void)
{
	Zombie* zombie;

	zombie = newZombie("HeapZombie");
	zombie->announce();

	randomChump("StackZombie");

	delete zombie;

	return 0;
}
