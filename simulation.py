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
        #self.total_infected = 0 # Int
        self.current_infected = 0 # Int    counts number of infected
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []   #stores infected people
        

        self.logger = Logger(self.file_name)
        self.population = self._create_population(initial_infected)
        self.simulation = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    # DONE
    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''

        population = []
        self.current_infected = 0
        vaccinated = 0
        id = 0

        while len(population) != pop_size:
            if self.initial_infected != self.current_infected:
                population = Person(id, is_vaccinated = False, infection = virus) #infected
                self.current_infected+=1
                id+=1
            else:
                if random.random() < self.vacc_percentage:
                    population.append(Person(id, is_vaccinated=True)) #vaccinated / unaffected
                    vaccinated+=1
                    id+=1
                else:
                    population.append(Person(id, is_vaccinated=False)) #infected / sick
                    self.current_infected+=1
                    id+=1
        return population

    # DONE
    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        if self.current_infected == 0 or vacc_percentage < 1:
            return True
        else:
            return False

    # DONE
    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        
        time_step_number = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            self.time_step()
            should_continue = self._simulation_should_continue()
            time_step_number +=1
            self.logger.log_time_step(time_step_number)
            print('The simulation has ended after {time_step_number} turns.'.format(time_step_number))
            pass

    # DONE
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
        interaction = 0
        while interaction < 100:
            for person in self.population:
                if person.is_alive == True and person.is_infected == True:
                    random_person = random.choice(self.population)
                    interacting=True
                    while interacting:
                        self.simulation.interaction(person, random_person)
                        interaction+=1
                        interacting=False
                    random_person = random.choice(self.population)
        
        self._infect_newly_infected()
    
    # DONE - needs logger edits
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
        
        #need to edit write to log
        if random_person.is_vaccinated == True:
            self.logger.log_interaction(self, person, random_person, random_person_sick=None, random_person_vacc=None, did_infect=None)
            return None
        elif random_person.is_infected == True:
            self.logger.log_interaction(self, person, random_person, random_person_sick=None, random_person_vacc=None, did_infect=None)
            return None
        elif random_person.is_infected and random_person.is_vaccinated == False:
            rand_num = random.randint(0,1)
            if rand_num <= repro_rate:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(self, person, random_person, random_person_sick=None, random_person_vacc=None, did_infect=None)
    
    # DONE
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
    sim = Simulation(pop_size, vacc_percentage,  initial_infected)

    sim.run()

#Terminal Inout order
    # Virus Name, Reproduction Rate, Mortality Rate, Population Size, Vaccincation Percentage, Initial Infected
    # EXAMPLE:  python3 simulation.py Ebola 0.25 0.70 100000 0.90 10           