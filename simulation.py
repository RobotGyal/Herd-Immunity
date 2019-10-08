import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
import os


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.
 
    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__ (self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''

        self.population = []# List of Person objects / 
        self.pop_size = pop_size # Int / 
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []


        self.logger = Logger(self.file_name)
        self.population = self._create_population(initial_infected)
        self.simulation = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    # need logic
    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''

        population = []
        infected_amount = 0
        new_id = None

        while len(population) != pop_size:
            if self.initial_infected != infected_amount:
                population = Person(new_id, is_vaccinated = False, infection = self.virus)
            else:
                pass      
        return population

    # √ but needs work
    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        for person in self.pop_size:
            if person.is_infected or len(self.total_dead) == len(self.pop_size):
                return True
            else:
                return False


    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        
        time_step_counter = 0
        should_continue = None

        while should_continue:
            print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))
            pass

    # √ finished todos - needs debug/test
    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        iteration = None
        while iteration <= 100:
            if person.is_alive == False or random_person.is_alive == False:
                next_person_id = randint(0,1)
            else:
                self.simulation.interaction(person, random_person)
                iteration +=1
    
    # √ finished todos - needs debug/test
    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True
        
        if random_person.is_vaccinated == True:
            continue
        elif random_person.is_infected == True:
            continue
        elif random_person.is_vaccinated and random_person.is_vaccinated == False:
            rand_num = random.randint(0,1)
            if rand_num <= repro_rate:
                self.newly_infected.append(random_person._id)
    
    # √ finished todos - needs debug/test
    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        for person in self.newly_infected:
            person.infect(self.virus)


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])
    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()

#Terminal Inout order
    # Virus Name, Reproduction Rate, Mortality Rate, Population Size, Vaccincatin Percentage, Initial Infected
    # EXAMPLE:  python3 simulation.py Ebola 0.25 0.70 100000 0.90 10           